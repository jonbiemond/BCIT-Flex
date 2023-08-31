"""SQLAlchemy Models Base Class"""
from __future__ import annotations

from typing import TypeVar

from sqlalchemy import inspect
from sqlalchemy.orm import DeclarativeBase, Mapper

_T = TypeVar("_T", bound="Base")


def db_to_attr(cls_mapper: Mapper, db_name: str) -> str:
    """Return the attribute name from the database name of a column."""
    for attr in cls_mapper.attrs:
        if type(attr).__name__ == "ColumnProperty":
            if attr.key == db_name:
                return attr.key
            elif cls_mapper.c[attr.key].name == db_name:
                return attr.key
    raise ValueError(f"Unknown database name: {db_name}")


def get_pks(obj, new_pk_vals: int | str | tuple | dict | None) -> dict:
    """Return a dict of primary keys updated with new_pk_vals."""

    cls_mapper = inspect(obj.__class__)

    pk_columns = [db_to_attr(cls_mapper, c.key) for c in cls_mapper.primary_key]
    if not isinstance(new_pk_vals, dict):
        # coerce pk_id to tuple
        if isinstance(new_pk_vals, (int, str)) or new_pk_vals is None:
            new_pk_vals = (new_pk_vals,)
        # get the primary key column names
        new_pk_vals = dict(zip(pk_columns, new_pk_vals))

    # update only keys that are in the primary key
    pk_ids = {c: getattr(obj, c) for c in pk_columns}
    pk_ids.update((k, new_pk_vals[k]) for k in new_pk_vals.keys() & pk_ids.keys())

    return pk_ids


class Base(DeclarativeBase):
    """Base class for SQLAlchemy model definitions."""

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
        include_relationships will clone FK relationships recursively if True.

        :param pk_id: primary key value, tuple or dict of primary key values corresponding to the primary key columns
        :param include_relationships: clone FK relationship attributes recursively if True
        :param kwargs: attributes to update
        """

        obj_mapper = inspect(self)
        cls_mapper = inspect(self.__class__)

        pk_attrs = [db_to_attr(cls_mapper, c.key) for c in cls_mapper.primary_key]

        # check if the object is loaded
        if not obj_mapper.persistent:
            raise ValueError("Object must be loaded before cloning.")

        # combine pk_id and kwargs
        updated = get_pks(self, pk_id)
        updated.update(kwargs)

        # raise error if any PKs without defaults are not updated
        required_pks = {
            c.key
            for c in cls_mapper.primary_key
            if c.server_default or c.default is None
        }
        passed_pks = {k for k, v in updated.items() if v is not None}
        if required_pks - passed_pks:
            raise ValueError(
                f"Missing required primary key columns: {required_pks - passed_pks}"
            )

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
                    # skip write_only and read_only relationships
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
