"""Course Blueprint"""

from flask import Blueprint, render_template, request
from sqlalchemy import select

from bcitflex.app_functions import filter_courses
from bcitflex.db import DBSession
from bcitflex.model import Course

bp = Blueprint("course", __name__)


@bp.route("/")
@bp.route("/courses", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        subject = request.form.get("subject")
        course_code = request.form.get("course_code")
        available = request.form.get("available")

        courses = filter_courses(
            session=DBSession,
            subject=subject,
            course_code=course_code,
            available=available,
        )
    else:
        courses = DBSession.scalars(select(Course)).all()
    return render_template("courses/index.html", courses=courses)


@bp.route("/courses/<int:course_id>")
def show(course_id):
    course = DBSession.get(Course, course_id)
    return render_template("courses/course.html", course=course)
