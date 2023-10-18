"""Alembic migration utility functions."""


def soft_delete_rule_ddl(tablename: str) -> str:
    """Generate the DDL for a soft delete rule.

    Args:
        tablename: The name of the table to generate the DDL for.

    Returns:
        The DDL for the soft delete rule.
    """
    return f"""
        CREATE RULE "_soft_delete" AS ON DELETE TO "{tablename}" DO INSTEAD (
            UPDATE {tablename} SET deleted_at = NOW() WHERE {tablename}_id = OLD.{tablename}_id AND deleted_at IS NULL
        );
    """
