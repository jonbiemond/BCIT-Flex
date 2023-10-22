"""Program Blueprint"""

from flask import Blueprint, render_template
from sqlalchemy import select

from bcitflex.db import DBSession
from bcitflex.model import Program

bp = Blueprint("program", __name__)


@bp.route("/programs")
def index():
    programs = DBSession.scalars(select(Program).order_by(Program.name)).all()
    return render_template("programs/index.html", programs=programs)


@bp.route("/programs/<int:program_id>")
def show(program_id):
    program = DBSession.get(Program, program_id)
    return render_template("programs/program.html", program=program)
