from typing import Optional

from src.domain.user import User
from src.ports.user_repository import UserRepository

from .database import close_connection, get_connection
from .mappers import row_to_user, user_to_row


class SQLiteUserRepository(UserRepository):
    def __init__(self, db_path: str = "ticketing.db"):
        self.db_path = db_path

    def save(self, user: User) -> User:
        conn = get_connection(self.db_path)
        cursor = conn.cursor()
        row = user_to_row(user)

        cursor.execute(
            """
            INSERT OR REPLACE INTO users
            (id, username, is_agent, is_admin)
            VALUES (?, ?, ?, ?)
            """,
            tuple(row.values()),
        )
        conn.commit()
        close_connection(conn)
        return user

    def get_by_id(self, user_id: str) -> Optional[User]:
        conn = get_connection(self.db_path)
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        row = cursor.fetchone()
        close_connection(conn)

        if row is None:
            return None

        return row_to_user(dict(row))

    def find_by_username(self, username: str) -> Optional[User]:
        conn = get_connection(self.db_path)
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        row = cursor.fetchone()
        close_connection(conn)

        if row is None:
            return None

        return row_to_user(dict(row))

    def list_all(self) -> list[User]:
        conn = get_connection(self.db_path)
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM users")
        rows = cursor.fetchall()
        close_connection(conn)

        return [row_to_user(dict(row)) for row in rows]
