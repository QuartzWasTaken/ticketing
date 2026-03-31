import pytest

from src.adapters.db.database import init_database
from src.adapters.db.ticket_repository_sqlite import SQLiteTicketRepository
from src.adapters.db.user_repository_sqlite import SQLiteUserRepository


@pytest.fixture
def sqlite_ticket_repo(tmp_path):
    """
    Fixture fournissant un repository SQLite de tickets avec une base temporaire.
    """
    db_path = tmp_path / "test.db"
    init_database(str(db_path))
    return SQLiteTicketRepository(str(db_path))


@pytest.fixture
def sqlite_user_repo(tmp_path):
    """Cree un UserRepository SQLite avec une base temporaire."""
    db_path = tmp_path / "test_users.db"
    init_database(str(db_path))
    return SQLiteUserRepository(str(db_path))
