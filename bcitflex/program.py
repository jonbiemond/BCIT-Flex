"""Program Blueprint"""

from flask import Blueprint, flash, g, render_template, request, session
from sqlalchemy import select

from bcitflex.db import DBSession
from bcitflex.model import Program

bp = Blueprint("program", __name__)


@bp.route("/programs")
def index():
    programs = DBSession.scalars(select(Program).order_by(Program.name)).all()
    return render_template("programs/index.html", programs=programs)


@bp.route("/programs/<int:program_id>", methods=["POST", "GET"])
def show(program_id):
    program = DBSession.get(Program, program_id)
    if request.method == "POST":
        programs = session.get("programs", [])
        if request.form.get("favourite"):
            if g.user is not None:
                g.user.preference.programs.append(program_id)
                DBSession.commit()
            programs.append(program_id) if program_id not in programs else None
            flash("Program added to favourites.")
        else:
            if g.user is not None:
                g.user.preference.programs.remove(program_id)
                DBSession.commit()
            programs.remove(program_id)
            flash("Program removed from favourites.")
        session["programs"] = programs
    return render_template(
        "programs/program.html", program=program, favourites=session.get("programs", [])
    )
