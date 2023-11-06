"""Course Blueprint"""

from flask import Blueprint, render_template, request
from sqlalchemy import not_, select

from bcitflex.app_functions import ModelFilter
from bcitflex.db import DBSession
from bcitflex.model import Course, Meeting, Offering, Subject, Term
from bcitflex.model.offering import NOT_AVAILABLE

bp = Blueprint("course", __name__)


@bp.route("/")
@bp.route("/courses", methods=["GET", "POST"])
def index():
    filters = ModelFilter(Course)
    if request.method == "POST":
        filters.where(Offering.term_id == request.form.get("term"))
        filters.where(Course.subject_id == request.form.get("subject"))
        filters.where(Meeting.campus == request.form.get("campus"), links=[Offering])
        filters.where(Course.code == request.form.get("code"))
        if name := request.form.get("name"):
            filters.where(Course.name.ilike("%" + name + "%"))
        if request.form.get("available") is not None:
            filters.where(not_(Offering.status.in_(NOT_AVAILABLE)))
    courses = DBSession.scalars(filters.stmt).all()
    subjects = DBSession.scalars(select(Subject).where(Subject.is_active)).all()
    terms = DBSession.scalars(select(Term).join(Offering)).unique().all()
    locations = DBSession.scalars(select(Meeting.campus).distinct()).all()
    return render_template(
        "courses/index.html",
        courses=courses,
        subjects=subjects,
        terms=terms,
        locations=locations,
    )


@bp.route("/courses/<int:course_id>")
def show(course_id):
    course = DBSession.get(Course, course_id)
    return render_template("courses/course.html", course=course)
