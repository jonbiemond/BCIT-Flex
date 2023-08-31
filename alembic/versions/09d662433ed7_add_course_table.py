"""Add course table

Revision ID: 09d662433ed7
Revises: 86cd0f1798a8
Create Date: 2023-07-30 07:59:06.045086

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "09d662433ed7"
down_revision = "86cd0f1798a8"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute(sa.schema.CreateSequence(sa.Sequence("course_course_id_seq")))
    op.create_table(
        "course",
        sa.Column(
            "course_id",
            sa.Integer(),
            nullable=False,
            comment="Serial course ID.",
        ),
        sa.Column(
            "subject_id",
            sa.String(),
            nullable=False,
            comment="Subject code, e.g. COMP.",
        ),
        sa.Column("code", sa.String(), nullable=False, comment="Course code."),
        sa.Column(
            "name",
            sa.String(length=100),
            nullable=False,
            comment="Course name.",
        ),
        sa.Column(
            "prerequisites",
            sa.String(length=100),
            nullable=False,
            comment="Prerequisites as strings.",
        ),
        sa.Column(
            "credits",
            sa.Float(precision=2),
            nullable=False,
            comment="Credit hours.",
        ),
        sa.Column("url", sa.String(length=100), nullable=False, comment="URL."),
        sa.PrimaryKeyConstraint("course_id"),
        comment="Courses.",
    )
    op.add_column("offering", sa.Column("course_id", sa.Integer(), nullable=False))
    op.create_foreign_key(
        "offering_course_id_fkey", "offering", "course", ["course_id"], ["course_id"]
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint("offering_course_id_fkey", "offering", type_="foreignkey")
    op.drop_column("offering", "course_id")
    op.drop_table("course")
    op.execute("DROP SEQUENCE course_course_id_seq")
    # ### end Alembic commands ###
