"""Course Blueprint"""

from flask import Blueprint, render_template, request
from sqlalchemy import select
from werkzeug.datastructures import ImmutableMultiDict

from bcitflex.app_functions import ModelFilter
from bcitflex.db import DBSession
from bcitflex.model import Course

bp = Blueprint("course", __name__)


def filters_from_form(form: ImmutableMultiDict) -> ModelFilter:
    """Return a list of CourseFilters from the given form."""
    filters = ModelFilter(Course)
    filters.add_condition("subject_id", form.get("subject"))
    filters.add_condition("code", form.get("code"))
    filters.add_condition("is_available", form.get("available") == "True" or None)
    return filters


@bp.route("/")
@bp.route("/courses", methods=["GET", "POST"])
def index():
    courses = DBSession.scalars(select(Course)).all()
    if request.method == "POST":
        print(request.form)
        courses = filters_from_form(request.form).filter(courses)
    return render_template("courses/index.html", courses=courses)


@bp.route("/courses/<int:course_id>")
def show(course_id):
    course = DBSession.get(Course, course_id)
    return render_template("courses/course.html", course=course)
