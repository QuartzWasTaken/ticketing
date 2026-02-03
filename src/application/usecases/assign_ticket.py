"""
Use case : Assigner un ticket à un agent.

Ce use case gère l'assignation d'un ticket existant à un agent.
"""

from src.domain.exceptions import TicketNotFoundError
from src.domain.ticket import Ticket
from src.ports.ticket_repository import TicketRepository


class AssignTicketUseCase:
    """
    Cas d'usage pour assigner un ticket à un agent.
    """

    def __init__(self, ticket_repo: TicketRepository):
        """
        Initialise le use case.

        Args:
            ticket_repo: Le repository de tickets
        """
        self.repo = ticket_repo
        # TODO: Stocker le repository en attribut

    def execute(self, ticket_id: str, agent_id: str) -> Ticket:
        """
        Assigne un ticket à un agent.

        Args:
            ticket_id: ID du ticket à assigner
            agent_id: ID de l'agent assigné

        Returns:
            Le ticket mis à jour

        Raises:
            TicketNotFoundError: Si le ticket n'existe pas
        """

        # TODO: Récupérer le ticket depuis le repository
        tik = self.repo.get_by_id(ticket_id)

        # TODO: Vérifier que le ticket existe (lever TicketNotFoundError sinon)
        if tik is None:
            raise TicketNotFoundError

        # TODO: Appeler la méthode assign() du ticket avec agent_id
        Ticket.assign(tik, agent_id)

        # TODO: Sauvegarder le ticket modifié
        self.repo.save(tik)

        # TODO: Retourner le ticket mis à jour
        return tik
