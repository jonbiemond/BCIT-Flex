"""Add term table

Revision ID: c3592c25409c
Revises: 96a6aafa05d6
Create Date: 2023-08-07 06:19:36.132870

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "c3592c25409c"
down_revision = "96a6aafa05d6"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "term",
        sa.Column("term_id", sa.String(length=6), nullable=False, comment="Term ID."),
        sa.Column("year", sa.Integer(), nullable=False, comment="Term year."),
        sa.Column(
            "season",
            sa.String(length=20),
            nullable=False,
            comment="Term season.",
        ),
        sa.PrimaryKeyConstraint("term_id"),
        comment="Offering terms.",
    )
    op.add_column("offering", sa.Column("term_id", sa.String(length=6), nullable=False))
    op.create_foreign_key(
        "offering_term_id_fkey", "offering", "term", ["term_id"], ["term_id"]
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint("offering_term_id_fkey", "offering", type_="foreignkey")
    op.drop_column("offering", "term_id")
    op.drop_table("term")
    # ### end Alembic commands ###
