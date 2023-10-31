"""Account Blueprint"""

from flask import Blueprint, g, render_template
from sqlalchemy import select

from bcitflex.auth import login_required
from bcitflex.db import DBSession
from bcitflex.model import Program

bp = Blueprint("account", __name__)


@bp.route("/account")
@login_required
def index():
    programs = DBSession.scalars(
        select(Program).where(Program.program_id.in_(g.user.preference.programs))
    ).all()
    return render_template("account/account.html", programs=programs)
