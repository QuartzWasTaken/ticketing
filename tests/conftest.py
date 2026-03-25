import pytest

from src.adapters.db.database import init_database
from src.adapters.db.ticket_repository_sqlite import SQLiteTicketRepository


@pytest.fixture
def sqlite_ticket_repo(tmp_path):
    """
    Fixture fournissant un repository SQLite de tickets avec une base temporaire.
    """
    db_path = tmp_path / "test.db"
    init_database(str(db_path))
    return SQLiteTicketRepository(str(db_path))
