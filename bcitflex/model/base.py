"""SQLAlchemy Models Base Class"""
from __future__ import annotations

from typing import TypeVar

from sqlalchemy import (
    TIMESTAMP,
    Column,
    MetaData,
    UniqueConstraint,
    func,
    inspect,
    select,
)
from sqlalchemy.orm import DeclarativeBase, Mapper, Session
from sqlalchemy.orm import MappedAsDataclass as MappedAsDataclassBase

_T = TypeVar("_T", bound="Base")

# Constraint naming conventions
convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}


def db_to_attr(cls_mapper: Mapper, db_name: str) -> str:
    """Return the attribute name from the database name of a column."""
    for attr in cls_mapper.attrs:
        if type(attr).__name__ == "ColumnProperty":
            if attr.key == db_name:
                return attr.key
            elif cls_mapper.c[attr.key].name == db_name:
                return attr.key
    raise ValueError(f"Unknown database name: {db_name}")


def updated_pks(obj: _T, new_pk_vals: dict) -> dict:
    """Return a dict of primary keys updated with new_pk_vals."""

    cls_mapper = inspect(obj.__class__)

    pk_columns = {db_to_attr(cls_mapper, c.key): c for c in cls_mapper.primary_key}
    pk_vals = {key: getattr(obj, key) for key in pk_columns.keys()}

    # update only keys that are in the primary key
    for k in new_pk_vals.keys():
        # fall back to existing value if new value is None and there is no default
        default_val = (
            None
            if pk_columns[k].default or pk_columns[k].server_default
            else pk_vals[k]
        )
        pk_vals[k] = new_pk_vals[k] or default_val

    return pk_vals


class Base(DeclarativeBase):
    """Base class for SQLAlchemy model definitions."""

    metadata = MetaData(naming_convention=convention)

    @classmethod
    def _unique_constraint(
        cls: "_T",
        constraint_name: str | None = None,
    ) -> UniqueConstraint | None:
        """Return the unique constraint of a model."""
        mapper = inspect(cls)

        uq_constraints = [
            constraint
            for constraint in mapper.persist_selectable.constraints
            if isinstance(constraint, UniqueConstraint)
        ]

        if not uq_constraints:
            return None

        if constraint_name is not None:
            uq_constraint = next(
                (
                    constraint
                    for constraint in uq_constraints
                    if constraint.name == constraint_name
                ),
                None,
            )
            if uq_constraint is None:
                raise ValueError(
                    f"{cls.__name__} model has no unique constraint named {constraint_name}."
                )
        else:
            if len(uq_constraints) > 1:
                raise ValueError(
                    f"{cls.__name__} model has multiple unique constraints. Must specify constraint_name."
                )
            uq_constraint = uq_constraints[0]

        return uq_constraint

    @classmethod
    def get_by_unique(
        cls: "_T",
        session: Session,
        unique_id: int | str | tuple,
        constraint_name: str | None = None,
    ) -> _T | None:
        """
        Return an object using the unique constraint instead of the primary key.

        Model must have a unique constraint defined,
        and the number of unique id values must match the number of unique columns.
        Return exactly one scalar result or None.
        Raise an exception in the case of multiple results,
        because the unique constraint may not be enforced in the database.

        :param session: SQLAlchemy session
        :param unique_id: unique id value or tuple of unique id values corresponding to the unique columns
        :param constraint_name: unique constraint name, optional

        :return: scalar result or None

        :raises ValueError: if the model has no unique fields
        """

        # coerce unique_id to tuple
        if isinstance(unique_id, (int, str)):
            unique_id = (unique_id,)

        # get the unique column names
        uq_constraint = cls._unique_constraint(constraint_name)
        if uq_constraint is None:
            raise ValueError(f"{cls.__name__} model has no unique constraints.")

        unique_columns = [c.key for c in uq_constraint.columns]

        # get the object matching the unique id
        filters = dict(zip(unique_columns, unique_id))
        stmt = select(cls).filter_by(**filters)
        return session.execute(stmt).scalar_one_or_none()

    def clone(
        self,
        pk_id: int | str | tuple | dict | None = None,
        include_relationships: bool = True,
        **kwargs,
    ) -> _T:
        """
        Clone the object with the given primary key and kwargs including FK relationships.

        Update the primary key and any other attributes passed as kwargs.
        Leave pk_id as None and SQLAlchemy will default to default if defined.
        If pk_id is a tuple, it must match the number of primary key columns.
        include_relationships will clone FK relationships recursively if True and object is attached to a session.

        :param pk_id: primary key value, tuple or dict of primary key values corresponding to the primary key columns
        :param include_relationships: clone FK relationship attributes recursively if True
        :param kwargs: attributes to update
        """

        obj_mapper = inspect(self)
        cls_mapper = inspect(self.__class__)

        pk_attrs = [db_to_attr(cls_mapper, c.key) for c in cls_mapper.primary_key]

        # omit relationships if object is not attached to a session
        if not obj_mapper.persistent:
            include_relationships = False

        # coerce pk_id to dict
        if not isinstance(pk_id, dict):
            # extract new pk vals from kwargs if not passed
            if pk_id is None:
                pk_id = {k: kwargs.pop(k) for k in pk_attrs if k in kwargs}
            # coerce pk_id to tuple
            elif isinstance(pk_id, (int, str)):
                pk_id = (pk_id,)
                # get the primary key column names
                pk_id = dict(zip(pk_attrs, pk_id))

        # TODO: validate pk_id

        # set missing pk values to None
        pk_id = {k: pk_id.get(k) for k in pk_attrs}

        # combine pk_id and kwargs
        updated = updated_pks(self, pk_id)
        updated.update(kwargs)

        # get model columns and values
        data = {
            column: getattr(self, column)
            for column in cls_mapper.columns.keys()
            if column not in pk_attrs
        }

        # get model relationships and values
        if include_relationships:
            for attr in cls_mapper.attrs:
                if type(attr).__name__ == "ColumnProperty":
                    continue

                elif type(attr).__name__ == "Relationship":
                    # skip write_only and viewonly relationships
                    if attr.lazy == "write_only" or attr.viewonly:
                        continue

                    remote_cls_mapper = attr.mapper

                    # skip relationships that where the parent key is on the remote side
                    remote_pk_columns = {c.key for c in remote_cls_mapper.primary_key}
                    remote_columns = {c.key for c in attr.remote_side}
                    if remote_pk_columns == remote_columns:
                        continue

                    # if there are no updated columns on the right side, don't clone
                    if not any(c in attr.mapper.column_attrs for c in updated.keys()):
                        data[attr.key] = getattr(self, attr.key)
                        continue

                    # get the updated relationship columns and values
                    updated_rel_vals = {
                        c.key: None
                        for c in remote_cls_mapper.primary_key
                        if c.server_default is not None
                    }
                    rel_attrs = [
                        db_to_attr(cls_mapper, c.key) for c in attr.local_columns
                    ]
                    rel_data = {c: updated[c] for c in rel_attrs if c in updated}
                    updated_rel_vals.update(rel_data)

                    # don't recurse more than one level if relationship is Many-to-Many
                    recurse = attr.direction.name != "MANYTOMANY"

                    # iterate over a collection and clone
                    # alternatively, attr.uselist
                    if attr.collection_class is not None:
                        collection = attr.collection_class()
                        for obj in getattr(self, attr.key):
                            collection.append(
                                obj.clone(
                                    include_relationships=recurse,
                                    **updated_rel_vals,
                                )
                            )
                        data[attr.key] = collection

                    else:
                        obj = getattr(self, attr.key)
                        if obj is not None:
                            data[attr.key] = obj.clone(**updated_rel_vals)

                else:
                    raise ValueError(f"Unhandled attribute type: {type(attr).__name__}")

        # update attributes
        data.update(updated)

        # create a new object
        cls = type(self)
        return cls(**data)


class MappedAsDataclass(MappedAsDataclassBase):
    """MappedAsDataclass with getitem."""

    def __getitem__(self, field):
        return getattr(self, field)


class TimestampsMixin:
    """Define timestamp columns."""

    __abstract__ = True

    __created_at_name__ = "created_at"
    __updated_at_name__ = "updated_at"
    __datetime_func__ = func.now()

    created_at = Column(
        __created_at_name__,
        TIMESTAMP(timezone=True),
        default=__datetime_func__,
        server_default=__datetime_func__,
        nullable=False,
    )

    updated_at = Column(
        __updated_at_name__,
        TIMESTAMP(timezone=True),
        default=__datetime_func__,
        onupdate=__datetime_func__,
        server_default=__datetime_func__,
        nullable=False,
    )
