"""Add soft delete rules

Revision ID: f8ac7b4c05a9
Revises: ee39506eab40
Create Date: 2023-10-14 04:34:49.974730

"""
from alembic import op
import sqlalchemy as sa

from bcitflex.alembic.utils import soft_delete_rule_ddl


# revision identifiers, used by Alembic.
revision = "f8ac7b4c05a9"
down_revision = "ee39506eab40"
branch_labels = None
depends_on = None

TABLES = [
    "course",
    "subject",
    "term",
]


def upgrade() -> None:
    for table in TABLES:
        op.execute(soft_delete_rule_ddl(table))

    op.execute(
        """
        CREATE RULE "_soft_delete" AS ON DELETE TO "offering" DO INSTEAD (
            UPDATE offering SET deleted_at = NOW() WHERE crn = OLD.crn AND deleted_at IS NULL
        );
    """
    )
    op.execute(
        """
        CREATE RULE "_soft_delete" AS ON DELETE TO "meeting" DO INSTEAD (
            UPDATE meeting SET deleted_at = NOW() WHERE meeting_id = OLD.meeting_id AND crn = OLD.crn AND deleted_at IS NULL
        );
    """
    )

    op.execute(
        """
        CREATE RULE "_soft_delete" AS ON DELETE TO "user" DO INSTEAD (
            UPDATE "user" SET deleted_at = NOW() WHERE id = OLD.id AND deleted_at IS NULL
        );
    """
    )


def downgrade() -> None:
    TABLES.extend(["offering", "meeting", "user"])
    for table in TABLES:
        op.execute(f"ALTER TABLE {table} DROP RULE _soft_delete;")
