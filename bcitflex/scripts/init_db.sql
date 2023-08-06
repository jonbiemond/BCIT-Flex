/*
Create the database and role.
Requires superuser.
Replace <password> with a password of your choice, and store it in .pgpass.

Once the database is created, to build the schema, run:
> alembic upgrade head
 */

CREATE DATABASE bcitflex;
CREATE ROLE python_app WITH LOGIN PASSWORD <'password'>;
\c bcitflex
GRANT ALL ON SCHEMA public TO python_app;
