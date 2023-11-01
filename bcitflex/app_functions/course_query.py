"""Filter courses."""
from typing import Type

from functional import seq
from sqlalchemy import Column, inspect

from bcitflex.model import Base, Course, Subject
from bcitflex.model.enum import Match

NOT_AVAILABLE = ["Full", "In Progress", "Cancelled", "Closed", "Waitlist"]


def coerce_to_column_type(model_column: Column, value: str | int) -> str | int:
    """Coerce a value to the type of the given model column."""
    column_data_type = model_column.type.python_type
    return column_data_type(value)


class ModelFilter:
    def __init__(self, model: Type[Base]):
        self.conditions: list[callable] = []
        self.model = model
        self.mapper = inspect(model)
        self.relationships = {
            relationship.mapper.class_: relationship.key
            for relationship in self.mapper.relationships
        }

    def __call__(self, obj: Type[Base]) -> bool:
        return all(condition(obj) for condition in self.conditions)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.conditions})"

    def add_condition(
        self,
        attr: str,
        value: str | int | None,
        relation: Type[Base] | None = None,
        match: Match = Match.EXACT,
    ):
        """Return a function that returns True if the given model attribute
        matches the given value.
        """

        if value is None or value == "":
            return

        attr_model = relation or self.model
        attr_model_mapper = inspect(attr_model)
        if attr in attr_model_mapper.columns:
            model_column = attr_model_mapper.columns[attr]
            value = coerce_to_column_type(model_column, value)

        if relation is not None:
            rel_key = self.relationships[relation]

            if self.mapper.relationships[rel_key].uselist:

                def condition(obj: Type[Base]) -> bool:
                    model_attr = getattr(obj, rel_key)
                    return any(getattr(item, attr) == value for item in model_attr)

            else:

                def condition(obj: Type[Base]) -> bool:
                    model_attr = getattr(getattr(obj, rel_key), attr)
                    return model_attr == value

        else:

            def condition(obj: Type[Base]) -> bool:
                model_attr = getattr(obj, attr)
                if match is Match.EXACT:
                    return model_attr == value
                else:
                    return value.lower() in model_attr.lower()

        self.conditions.append(condition)

    def filter(self, objs: list[Base]) -> list[Base]:
        """Return a list of objects that match the given criteria."""
        objs_seq = seq(objs)
        objs_seq = objs_seq.filter(self)
        return objs_seq.to_list()


if __name__ == "__main__":
    courses = [
        Course(code="1234", subject=Subject(subject_id="COMP")),
        Course(code="5678", subject=Subject(subject_id="COMP")),
    ]

    course_filter = ModelFilter(Course)
    course_filter.add_condition("subject_id", "COMP", Subject)
    course_filter.add_condition("code", "1234")
    filtered_courses = course_filter.filter(courses)
    print(filtered_courses)
