"""Course Blueprint."""

from flask import Blueprint, render_template, request, session
from sqlalchemy import not_, select

from bcitflex.app_functions import ModelFilter
from bcitflex.db import DBSession, db
from bcitflex.model import Course, Meeting, Offering, Program, Subject, Term
from bcitflex.model.offering import NOT_AVAILABLE

bp = Blueprint("course", __name__)


@bp.route("/")
@bp.route("/courses", methods=["GET"])
def index():
    """List courses."""

    # apply filters from get request
    filters = ModelFilter(Course)
    filters.where(Offering.term_id == request.args.get("term"))
    filters.where(Course.subject_id == request.args.get("subject"))
    filters.where(Meeting.campus == request.args.get("campus"), links=[Offering])
    filters.where(Course.code == request.args.get("code"))
    if (name := request.args.get("name")) is not None:
        filters.where(Course.name.ilike("%" + name + "%"))
    if request.args.get("available") is not None:
        filters.where(not_(Offering.status.in_(NOT_AVAILABLE)))

    # apply filters from session
    program_ids = session.get("programs") or []
    programs = list(
        DBSession.scalars(select(Program).where(Program.program_id.in_(program_ids)))
    )
    if program_ids and (request.args.get("favourites") is not None or not request.args):
        filters.where(Program.program_id.in_(program_ids), [Course.programs])

    courses = filters.stmt.order_by(Course.code)
    pagination = db.paginate(courses, per_page=25)
    subjects = DBSession.scalars(select(Subject).where(Subject.is_active)).all()
    terms = DBSession.scalars(select(Term).join(Offering)).unique().all()
    locations = DBSession.scalars(select(Meeting.campus).distinct()).all()
    return render_template(
        "courses/index.html",
        courses=courses,
        pagination=pagination,
        subjects=subjects,
        terms=terms,
        locations=locations,
        programs=programs,
    )


@bp.route("/courses/<subject_id>-<code>")
def show(subject_id, code):
    """Display course details."""
    course = Course.get_by_unique(DBSession, (subject_id.upper(), code))
    return render_template("courses/course.html", course=course)
