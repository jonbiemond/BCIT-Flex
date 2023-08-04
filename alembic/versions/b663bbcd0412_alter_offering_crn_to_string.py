"""Alter offering.crn to string

Revision ID: b663bbcd0412
Revises: 8cfa744d65d4
Create Date: 2023-08-04 12:54:03.308223

"""
from alembic import op
from sqlalchemy.schema import Sequence, CreateSequence, DropSequence
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "b663bbcd0412"
down_revision = "8cfa744d65d4"
branch_labels = None
depends_on = None

# sequence object
crn_seq = Sequence("offering_crn_seq")


def upgrade() -> None:
    op.alter_column(
        "offering",
        "crn",
        type_=sa.String(length=5),
        nullable=False,
        existing_comment="Course Reference Number, unique to offering.",
        server_default=None,
    )
    op.execute(DropSequence(crn_seq))


def downgrade() -> None:
    op.execute(CreateSequence(crn_seq))
    op.alter_column(
        "offering",
        "crn",
        type_=sa.Integer(),
        nullable=False,
        existing_comment="Course Reference Number, unique to offering.",
        postgresql_using="crn::integer",
        server_default=crn_seq.next_value(),
    )
