"""
Adaptateur SQLite pour le repository de tickets.

Implementation de TicketRepository avec persistance SQLite.
"""

from typing import Optional

from src.domain.ticket import Ticket
from src.ports.ticket_repository import TicketRepository

from .database import close_connection, get_connection
from .mappers import row_to_ticket, ticket_to_row


class SQLiteTicketRepository(TicketRepository):
    """Repository SQLite pour les tickets."""

    def __init__(self, db_path: str = "ticketing.db"):
        self.db_path = db_path

    def save(self, ticket: Ticket) -> Ticket:
        """Sauvegarde un ticket via INSERT OR REPLACE."""
        conn = get_connection(self.db_path)
        cursor = conn.cursor()
        row = ticket_to_row(ticket)

        cursor.execute(
            """
            INSERT OR REPLACE INTO tickets
            (id, title, description, creator_id, status, priority,
             assignee_id, project_id, created_at, updated_at, started_at, closed_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            tuple(row.values()),
        )
        conn.commit()
        close_connection(conn)
        return ticket

    def get_by_id(self, ticket_id: str) -> Optional[Ticket]:
        """Recupere un ticket par son ID."""
        conn = get_connection(self.db_path)
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM tickets WHERE id = ?", (ticket_id,))
        row = cursor.fetchone()
        close_connection(conn)

        if row is None:
            return None

        return row_to_ticket(dict(row))

    def list_all(self) -> list[Ticket]:
        """Retourne tous les tickets stockes en base."""
        conn = get_connection(self.db_path)
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM tickets")
        rows = cursor.fetchall()
        close_connection(conn)

        return [row_to_ticket(dict(row)) for row in rows]
