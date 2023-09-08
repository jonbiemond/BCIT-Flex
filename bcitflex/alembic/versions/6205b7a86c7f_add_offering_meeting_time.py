"""Add offering.meeting_time

Revision ID: 6205b7a86c7f
Revises: b663bbcd0412
Create Date: 2023-08-05 06:34:18.381120

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "6205b7a86c7f"
down_revision = "b663bbcd0412"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "offering",
        sa.Column(
            "meeting_time",
            sa.Text(),
            nullable=False,
            comment="Offering meeting time.",
        ),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("offering", "meeting_time")
    # ### end Alembic commands ###