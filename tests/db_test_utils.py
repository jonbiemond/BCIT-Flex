"""Utils for configuring and cleaning up test databases.

Source: pgcli https://github.com/dbcli/pgcli
"""
from os import getenv

import psycopg2
from sqlalchemy import engine

from alembic import config, script
from alembic.runtime import migration

POSTGRES_USER = getenv("PGUSER", "postgres")
POSTGRES_HOST = getenv("PGHOST", "localhost")
POSTGRES_PORT = getenv("PGPORT", 5432)
POSTGRES_PASSWORD = getenv("PGPASSWORD", "postgres")


def db_connection(dbname=None):
    """Get a psycopg2 connection to the database."""
    conn = psycopg2.connect(
        user=POSTGRES_USER,
        host=POSTGRES_HOST,
        password=POSTGRES_PASSWORD,
        port=POSTGRES_PORT,
        dbname=dbname,
    )
    conn.autocommit = True
    return conn


def create_db(dbname):
    """Create a database with the given name if it does not exist."""
    with db_connection().cursor() as cur:
        cur.execute(f"SELECT datname FROM pg_database WHERE datname = '{dbname}';")
        if not cur.fetchone():
            cur.execute(f"CREATE DATABASE {dbname};")


def drop_tables(conn):
    """Drop all tables in the public schema."""
    with conn.cursor() as cur:
        cur.execute(
            """
            DROP SCHEMA public CASCADE;
            CREATE SCHEMA public;"""
        )


def check_current_head(alembic_cfg: config.Config, connectable: engine.Engine) -> bool:
    """Check if the database is up-to-date with the latest migrations."""
    directory = script.ScriptDirectory.from_config(alembic_cfg)
    with connectable.begin() as connection:
        context = migration.MigrationContext.configure(connection)
        return set(context.get_current_heads()) == set(directory.get_heads())
