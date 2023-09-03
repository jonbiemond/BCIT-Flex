"""Flask application factory."""

import os

from flask import Flask


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev",
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # DB config
    from . import db

    db.init_app(app)

    # Auth blueprint
    from . import auth

    app.register_blueprint(auth.bp)

    # Course blueprint
    from . import course

    app.register_blueprint(course.bp)
    app.add_url_rule("/", endpoint="index")

    return app
