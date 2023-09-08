"""App db config"""
import secrets
import string
from pathlib import Path

import click
import psycopg2
from alembic import config, script
from alembic.runtime import migration
from flask import Flask, current_app
from sqlalchemy import engine

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
            cur.execute(f"CREATE DATABASE {dbname};")
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
    db_name,
    db_user,
    db_password,
    db_host="localhost",
    db_port=5432,
) -> str | None:
    """Save database url to instance config.py."""

    instance_path = Path(current_app.instance_path)
    config = instance_path / "config.py"

    # check if SQLALCHEMY_DATABASE_URI exists
    if config.exists():
        with open(config, "r") as f:
            lines = f.readlines()
            for line in lines:
                if "SQLALCHEMY_DATABASE_URI" in line:
                    return

    # write SQLALCHEMY_DATABASE_URI to config.py
    db_url = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
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
@click.option("--drop", is_flag=True, help="Clear existing schema.")
@click.option(
    "--name", "-n", default="bcitflex", show_default=True, help="Database name."
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
@click.option("--role", "-r", nargs=2, help="App role creds.   [default: python_app]")
def create_db_command(drop, name, host, port, superuser, role):
    """Create database."""

    # generate password for role
    alphabet = string.ascii_letters + string.digits
    password = "".join(secrets.choice(alphabet) for i in range(12))

    # get roles
    superuser = superuser
    role = role or ("python_app", password)

    # get connection factory
    db_connection = db_connection_factory(
        pguser=superuser[0],
        pgpassword=superuser[1],
        pghost=host,
        pgport=port,
    )

    # create db
    created = create_db(name, db_connection, drop=drop)
    if not created:
        click.echo(f"Database {name} already exists.")
        return
    click.echo(f"Database {name} created.")

    # create role
    with db_connection(name).cursor() as cur:
        # TODO: handle role already exists elegantly
        cur.execute(f"CREATE ROLE {role[0]} WITH LOGIN PASSWORD '{role[1]}';")
        cur.execute(f"GRANT ALL PRIVILEGES ON DATABASE {name} TO '{role}';")
    click.echo(f"Role {role[0]}  created.")
    click.echo(f"Please store password in a safe place: {role[1]}")

    # save db url to instance config.py
    db_url = config_db_url(name, *role, db_host=host, db_port=port)
    instance_path = current_app.instance_path
    if db_url is not None:
        click.echo(f"Database url saved to {instance_path}/config.py")
        click.echo(f"URL: {db_url}")
    else:
        click.echo(f"Database url already set in {instance_path}/config.py")


@click.command("upgrade-db")
def upgrade_db_command():
    """Run database migrations."""

    alembic_cfg = config.Config("././alembic.ini")
    if not check_current_head(alembic_cfg, db.engine):
        config.command.upgrade(alembic_cfg, "head")
        click.echo("Database upgraded.")
    else:
        click.echo("Database already up to date.")


def init_app(app: Flask):
    """Initialize app with database connection."""

    if app.config.get("SQLALCHEMY_DATABASE_URI") is not None:
        db.init_app(app)
    elif app.config.get("TESTING") is not True:
        raise RuntimeError("SQLALCHEMY_DATABASE_URI not set in config.py")

    app.cli.add_command(create_db_command)
    app.cli.add_command(load_db_command)
    app.cli.add_command(upgrade_db_command)
