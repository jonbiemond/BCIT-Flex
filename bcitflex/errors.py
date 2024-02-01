"""Error Blueprint"""

from flask import (
    Blueprint,
    render_template,
)

bp = Blueprint("errors", __name__)


def error_page(e):
    return render_template("errors/404.html"), 404
