"""App db config"""

from flask import Flask

from .scripts import load_db_command


def init_app(app: Flask):
    app.cli.add_command(load_db_command)
