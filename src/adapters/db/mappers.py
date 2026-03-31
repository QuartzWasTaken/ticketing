"""
Mappers pour la conversion entre entites du domaine et lignes de base de donnees.

Ce module fournit des fonctions pour convertir les entites Ticket vers/depuis
les representations de lignes SQLite.
"""

from datetime import datetime

from src.domain.priority import Priority
from src.domain.status import Status
from src.domain.ticket import Ticket
from src.domain.user import User


def ticket_to_row(ticket: Ticket) -> dict:
    """
    Convertit une entite Ticket du domaine en dictionnaire pour la base de donnees.

    Args:
        ticket: L'entite ticket a convertir

    Returns:
        Dictionnaire avec les noms de colonnes et valeurs prets pour insertion SQL
    """
    closed_at = getattr(ticket, "closed_at", None)

    return {
        "id": ticket.id,
        "title": ticket.title,
        "description": ticket.description,
        "creator_id": ticket.creator_id,
        "status": ticket.status.value,
        "priority": ticket.priority.value,
        "assignee_id": ticket.assignee_id,
        "project_id": getattr(ticket, "project_id", None),
        "created_at": ticket.created_at.isoformat(),
        "updated_at": ticket.updated_at.isoformat(),
        "started_at": ticket.started_at.isoformat() if ticket.started_at else None,
        "closed_at": closed_at.isoformat() if closed_at else None,
    }


def row_to_ticket(row: dict) -> Ticket:
    """
    Convertit une ligne de base de donnees en entite Ticket du domaine.

    Args:
        row: Dictionnaire representant une ligne de base de donnees

    Returns:
        Entite Ticket du domaine
    """
    created_at = datetime.fromisoformat(row["created_at"])
    updated_at = datetime.fromisoformat(row["updated_at"])
    started_at = (
        datetime.fromisoformat(row["started_at"]) if row["started_at"] else None
    )
    closed_at = datetime.fromisoformat(row["closed_at"]) if row["closed_at"] else None

    ticket = Ticket(
        id=row["id"],
        title=row["title"],
        description=row["description"],
        creator_id=row["creator_id"],
        created_at=created_at,
        updated_at=updated_at,
        priority=Priority(row["priority"]),
        assignee_id=row["assignee_id"],
        started_at=started_at,
    )

    ticket._status = Status(row["status"])
    setattr(ticket, "project_id", row["project_id"])
    setattr(ticket, "closed_at", closed_at)

    return ticket


def user_to_row(user: User) -> dict:
    """Convertit une entite User en dictionnaire pour SQLite."""
    return {
        "id": user.id,
        "username": user.username,
        "is_agent": 1 if user.is_agent else 0,
        "is_admin": 1 if user.is_admin else 0,
    }


def row_to_user(row: dict) -> User:
    """Convertit une ligne SQL en entite User."""
    return User(
        id=row["id"],
        username=row["username"],
        is_agent=bool(row["is_agent"]),
        is_admin=bool(row["is_admin"]),
    )
