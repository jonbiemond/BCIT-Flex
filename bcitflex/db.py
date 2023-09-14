"""App db config"""
import os
import secrets
import string
import warnings
from pathlib import Path

import click
import psycopg2
from alembic import config, script
from alembic.runtime import migration
from flask import Flask, current_app
from sqlalchemy import engine, text

from .ext.database import SQLAlchemy
from .model.base import Base
from .scripts import load_db_command

db = SQLAlchemy(model=Base)
DBSession = db.session


def db_connection_factory(
    pguser="postgres",
    pghost="localhost",
    pgpassword="postgres",
    pgport=5432,
):
    """Get a db connection generator."""

    def db_connection(dbname=None):
        conn = psycopg2.connect(
            user=pguser,
            host=pghost,
            password=pgpassword,
            port=pgport,
            dbname=dbname,
        )
        conn.autocommit = True
        return conn

    return db_connection


def create_db(dbname, db_connection, drop=False) -> bool:
    """Create an empty database with the given name if it does not exist.

    :param dbname: Name of the database to create.
    :param db_connection: A psycopg2 connection generator.
    :param drop: Drop all tables in the public schema.

    :return: True if database was created, False if it already exists.
    """
    new_db = False
    with db_connection().cursor() as cur:
        cur.execute(f"SELECT datname FROM pg_database WHERE datname = '{dbname}';")
        if not cur.fetchone():
            cur.execute(f"CREATE DATABASE {dbname} ENCODING = 'UTF8';")
            new_db = True
        elif drop:
            with db_connection(dbname).cursor() as db_cur:
                db_cur.execute(
                    """
                    DROP SCHEMA public CASCADE;
                    CREATE SCHEMA public;"""
                )

    return new_db


def config_db_url(
    db_name: str,
    db_user: str,
    db_password: str | None = None,
    db_host: str = "localhost",
    db_port: int = 5432,
    overwrite: bool = False,
) -> str | None:
    """Save database url to instance config.py."""

    instance_path = Path(current_app.instance_path)
    config = instance_path / "config.py"

    # check if SQLALCHEMY_DATABASE_URI exists
    if config.exists():
        with open(config, "r+") as f:
            lines = f.readlines()
            to_omit = None
            for idx, line in enumerate(lines):
                if "SQLALCHEMY_DATABASE_URI" in line:
                    if not overwrite:
                        return
                    else:
                        to_omit = idx
                        break
            if to_omit is not None:
                lines.pop(to_omit)
                f.seek(0)
                f.truncate()
                f.writelines(lines)

    # set password string
    if db_password is None:
        db_password = ""
    else:
        db_password = f":{db_password}"

    # write SQLALCHEMY_DATABASE_URI to config.py
    db_url = f"postgresql://{db_user}{db_password}@{db_host}:{db_port}/{db_name}"
    with open(config, "a") as f:
        f.write(f'SQLALCHEMY_DATABASE_URI = "{db_url}"\n')

    return db_url


def check_current_head(alembic_cfg: config.Config, connectable: engine.Engine) -> bool:
    """Check if the database is up-to-date with the latest migrations."""
    directory = script.ScriptDirectory.from_config(alembic_cfg)
    with connectable.begin() as connection:
        context = migration.MigrationContext.configure(connection)
        return set(context.get_current_heads()) == set(directory.get_heads())


@click.command("create-db")
@click.option("--drop", "-D", is_flag=True, help="Clear existing schema.")
@click.option("--overwrite", "-o", is_flag=True, help="Overwrite existing config.")
@click.option(
    "--dbname", "-d", default="bcitflex", show_default=True, help="Database name."
)
@click.option(
    "--host", "-h", default="localhost", show_default=True, help="Database host."
)
@click.option("--port", "-p", default=5432, show_default=True, help="Database port.")
@click.option(
    "--superuser",
    "-su",
    nargs=2,
    default=("postgres", "postgres"),
    show_default=True,
    help="Superuser creds.",
)
@click.option("--role-name", "-r", default="python_app", help="App role name.")
@click.option("--role-password", "-rp", help="App role password.   [default: random]")
def create_db_command(
    drop, overwrite, dbname, host, port, superuser, role_name, role_password
):
    """Create database."""

    # generate password for role
    alphabet = string.ascii_letters + string.digits
    password = "".join(secrets.choice(alphabet) for i in range(12))

    # get connection factory
    db_connection = db_connection_factory(
        pguser=superuser[0],
        pgpassword=superuser[1],
        pghost=host,
        pgport=port,
    )

    # create db
    created = create_db(dbname, db_connection, drop=drop)
    if not created:
        click.echo(f"Database {dbname} already exists.")
    else:
        click.echo(f"Database {dbname} created.")

    # create role
    with db_connection(dbname).cursor() as cur:
        cur.execute(
            f"SELECT rolname FROM pg_catalog.pg_roles WHERE rolname = '{role_name}';"
        )

        if cur.fetchone():
            click.echo(f"Role {role_name} already exists.")
            if role_password is None:
                click.echo(
                    "WARNING: Role password unknown please set in config.py or in .pgpass."
                )
        else:
            role_password = role_password or password
            cur.execute(
                f"CREATE ROLE {role_name} WITH LOGIN PASSWORD '{role_password}';"
            )
            click.echo(f"Role {role_name} created.")
            click.echo(f"Please store password in a safe place: {role_password}")

        cur.execute(f'GRANT ALL PRIVILEGES ON DATABASE {dbname} TO "{role_name}";')
        cur.execute(f'GRANT ALL ON SCHEMA public TO "{role_name}";')

    # save db url to instance config.py
    db_url = config_db_url(
        dbname,
        role_name,
        role_password,
        db_host=host,
        db_port=port,
        overwrite=overwrite,
    )
    instance_path = current_app.instance_path
    if db_url is not None:
        click.echo(f"Database url saved to {instance_path}/config.py")
        click.echo(f"URL: {db_url}")
    else:
        click.echo(f"Database url already set in {instance_path}\\config.py")


@click.command("upgrade-db")
def upgrade_db_command():
    """Run database migrations."""
    alembic_cfg_path = os.path.join(os.path.dirname(__file__), "alembic/alembic.ini")
    alembic_cfg = config.Config(alembic_cfg_path)
    if not check_current_head(alembic_cfg, db.engine):
        with db.engine.begin() as connection:
            alembic_cfg.attributes["connection"] = connection
            config.command.upgrade(alembic_cfg, "head")
        click.echo("Database upgraded.")
    else:
        click.echo("Database already up to date.")


@click.command("load-subjects")
def load_subjects_command():
    """Populate subject table."""

    # read populate_subject.sql
    directory = os.path.dirname(__file__)
    script_path = os.path.join(directory, "scripts/populate_subject.sql")
    with open(script_path, "r") as f:
        stmt = f.read()

    with DBSession() as session:
        session.execute(text(stmt))
        session.commit()


def init_app(app: Flask):
    """Initialize app with database connection."""

    if app.config.get("SQLALCHEMY_DATABASE_URI") is not None:
        db.init_app(app)
        app.cli.add_command(load_db_command)
        app.cli.add_command(upgrade_db_command)
        app.cli.add_command(load_subjects_command)
    elif app.config.get("TESTING") is not True:
        # TODO: logging might be neater here
        warnings.warn(
            "SQLALCHEMY_DATABASE_URI not set. App will not connect to db.", stacklevel=1
        )

    app.cli.add_command(create_db_command)
