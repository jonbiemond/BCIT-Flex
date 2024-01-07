"""Add prerequisite tables

Revision ID: db4d9a6c53f9
Revises: 6f25f0a31d7d
Create Date: 2023-12-11 19:06:05.566743

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "db4d9a6c53f9"
down_revision = "6f25f0a31d7d"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute(sa.schema.CreateSequence(sa.Sequence("prereq_and_id_seq")))
    op.execute(sa.schema.CreateSequence(sa.Sequence("prereq_or_id_seq")))
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "prereq_and",
        sa.Column(
            "id",
            sa.Integer(),
            server_default=sa.text("nextval('prereq_and_id_seq')"),
            nullable=False,
            comment="Serial prerequisite_and ID.",
        ),
        sa.Column(
            "course_id",
            sa.Integer(),
            nullable=False,
            comment="Parent course ID for which this is a prerequisite.",
        ),
        sa.Column(
            "prereq_no",
            sa.Integer(),
            nullable=False,
            comment="Serial prerequisite_and ID partitioned by course_id.",
        ),
        sa.Column("deleted_at", sa.TIMESTAMP(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(
            ["course_id"],
            ["course.course_id"],
            name=op.f("fk_prereq_and_course_id_course"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_prereq_and")),
        comment="All prerequisites that must be met for a course.",
    )
    op.create_unique_constraint(
        op.f("uq_prereq_and_course_id_prereq_no"),
        "prereq_and",
        ["course_id", "prereq_no"],
    )
    op.create_table(
        "prereq_or",
        sa.Column(
            "id",
            sa.Integer(),
            server_default=sa.text("nextval('prereq_or_id_seq')"),
            nullable=False,
            comment="Serial prerequisite_or ID.",
        ),
        sa.Column("prereq_and_id", sa.Integer(), nullable=False),
        sa.Column("course_id", sa.Integer(), nullable=False),
        sa.Column(
            "criteria",
            sa.String(length=100),
            nullable=True,
            comment="Criteria for prerequisite.",
        ),
        sa.Column("deleted_at", sa.TIMESTAMP(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(
            ["prereq_and_id"],
            ["prereq_and.id"],
            name=op.f("fk_prereq_prereq_or_and_id_prereq_and"),
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["course_id"],
            ["course.course_id"],
            name=op.f("fk_prereq_or_course_id_course"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_prereq_or")),
        comment="At least one prerequisite per prereq_and_id must be met.",
    )
    op.create_unique_constraint(
        op.f("uq_prereq_or_prereq_and_id_course_id"),
        "prereq_or",
        ["prereq_and_id", "course_id"],
    )
    op.add_column(
        "course",
        sa.Column(
            "prerequisites_raw",
            sa.Text(),
            comment="Prerequisites as strings.",
        ),
    )
    op.execute(
        """
        UPDATE course
        SET prerequisites_raw = prerequisites
        """
    )
    op.alter_column("course", "prerequisites_raw", nullable=False)
    op.drop_column("course", "prerequisites")
    # ### end Alembic commands ###

    op.execute(
        """
        CREATE RULE "_soft_delete" AS ON DELETE TO "prereq_and" DO INSTEAD (
            UPDATE "prereq_and" SET deleted_at = NOW() WHERE id = OLD.id AND deleted_at IS NULL
        );
    """
    )
    op.execute(
        """
        CREATE RULE "_soft_delete" AS ON DELETE TO "prereq_or" DO INSTEAD (
            UPDATE "prereq_or" SET deleted_at = NOW() WHERE id = OLD.id AND deleted_at IS NULL
        );
    """
    )


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "course",
        sa.Column(
            "prerequisites",
            sa.TEXT(),
            autoincrement=False,
            comment="Prerequisites as strings.",
        ),
    )
    op.execute(
        """
        UPDATE course
        SET prerequisites = prerequisites_raw
        """
    )
    op.alter_column("course", "prerequisites", nullable=False)
    op.drop_column("course", "prerequisites_raw")
    op.drop_table("prereq_or")
    op.drop_table("prereq_and")
    # ### end Alembic commands ###
    op.execute(sa.schema.DropSequence(sa.Sequence("prereq_or_id_seq")))
    op.execute(sa.schema.DropSequence(sa.Sequence("prereq_and_id_seq")))