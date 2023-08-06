"""Add nssequence_nextval function

Revision ID: d76d960b31d5
Revises: 6205b7a86c7f
Create Date: 2023-08-06 08:52:38.922612

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "d76d960b31d5"
down_revision = "6205b7a86c7f"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute(
        """
        CREATE OR REPLACE FUNCTION nssequence_nextval()
RETURNS trigger AS $$
DECLARE
    query text;
    nextval bigint;
BEGIN
    IF TG_NARGS != 2 THEN
        RAISE EXCEPTION '% did not supply nssequence_nextval with the required arguments.', TG_NAME;
    END IF;

    query := 'SELECT COALESCE(MAX(%I)::text, ''0'')::bigint + 1 FROM %I.%I WHERE %I = $1.%I'::text;
    EXECUTE format(
        query,
        TG_ARGV[0], -- MAX(%I)::text, the column holding the sequence
        TG_TABLE_SCHEMA, TG_TABLE_NAME, -- FROM %I.%I - the table we are working with
        TG_ARGV[1], TG_ARGV[1] -- %I = $1.%I -- the column with the sequence namespace. Ideally a parent entity's UUID.
    ) USING NEW INTO nextval;

    -- The property name is the first argument of the trigger function, so we need hstore to set it.
    -- See https://stackoverflow.com/questions/7711432/how-to-set-value-of-composite-variable-field-using-dynamic-sql/7782641#7782641
    NEW := NEW #= hstore(TG_ARGV[0]::text, nextval::text);

    RETURN NEW;
END
$$ LANGUAGE 'plpgsql';
"""
    )


def downgrade() -> None:
    op.execute("DROP FUNCTION nssequence_nextval();")
