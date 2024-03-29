"""Add user preference table

Revision ID: 6f25f0a31d7d
Revises: 7034009b08f2
Create Date: 2023-10-29 08:48:39.156160

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "6f25f0a31d7d"
down_revision = "7034009b08f2"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute(sa.schema.CreateSequence(sa.Sequence("user_preference_id_seq")))
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "user_preference",
        sa.Column(
            "id",
            sa.Integer(),
            server_default=sa.text("nextval('user_preference_id_seq')"),
            nullable=False,
            comment="Serial user preference ID.",
        ),
        sa.Column("user_id", sa.Integer(), nullable=False, comment="User ID."),
        sa.Column(
            "programs",
            postgresql.ARRAY(sa.Integer()),
            server_default="{}",
            nullable=False,
            comment="User selected program ids.",
        ),
        sa.Column("deleted_at", sa.TIMESTAMP(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["user.id"],
            name=op.f("fk_user_preference_user_id_user"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_user_preference")),
        comment="User preferences.",
    )
    # ### end Alembic commands ###
    # Add rows to user_preference table for existing users
    op.execute(
        """
        INSERT INTO user_preference (user_id)
        SELECT id FROM public.user;
    """
    )


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("user_preference")
    # ### end Alembic commands ###
    op.execute(sa.schema.DropSequence(sa.Sequence("user_preference_id_seq")))
