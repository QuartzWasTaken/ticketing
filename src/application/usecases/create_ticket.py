"""
Use case : Créer un ticket.

Ce use case orchestre la création d'un ticket en utilisant les entités du domaine
et le port TicketRepository, sans dépendre d'une implémentation concrète.
"""

import uuid

from src.domain.priority import Priority
from src.domain.ticket import Ticket
from src.ports.ticket_repository import TicketRepository


class CreateTicketUseCase:
    """
    Cas d'usage pour créer un nouveau ticket.

    Reçoit le repository via injection de dépendances (principe d'inversion).
    """

    def __init__(self, ticket_repo: TicketRepository):
        """
        Initialise le use case avec ses dépendances.

        Args:
            ticket_repo: Le repository (via son interface)
        """
        self.ticket_repo = ticket_repo

    def execute(self, title: str, description: str, creator_id: str) -> Ticket:
        """
        Exécute la création d'un ticket.

        Args:
            title: Titre du ticket
            description: Description du problème
            creator_id: ID de l'utilisateur créateur

        Returns:
            Le ticket créé

        Raises:
            ValueError: Si les données sont invalides
        """
        # Créer le ticket avec les entités du domaine
        ticket = Ticket(
            id=str(uuid.uuid4()),  # Génère un UUID
            title=title,
            description=description,
            creator_id=creator_id,
            priority=Priority.MEDIUM,
        )

        # Persister via le port (peu importe l'implémentation !)
        saved_ticket = self.ticket_repo.save(ticket)

        return saved_ticket
