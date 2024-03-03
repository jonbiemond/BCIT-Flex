"""Tests for the batch process model."""
import pytest
from sqlalchemy.orm import Session

from bcitflex.model import BatchProcess
from tests import dbtest


@pytest.fixture
def new_batch_process() -> BatchProcess:
    """Return a new batch process object."""
    return BatchProcess()


class TestBatchProcess:
    """Test the BatchProcess class."""

    def test_init(self, new_batch_process: BatchProcess):
        """Test the constructor."""
        assert new_batch_process.id is None
        assert new_batch_process.created_at is None


@dbtest
class TestBatchProcessDB:
    """Test the BatchProcessDB class with a database session."""

    def test_get_batch_process(self, db_session: Session):
        """Test getting a batch process from the db."""
        batch_process = db_session.get(BatchProcess, 1)
        assert batch_process.created_at is not None
