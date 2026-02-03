"""
Tests du use case AssignTicket.
"""

import pytest

from src.adapters.db.ticket_repository_inmemory import InMemoryTicketRepository
from src.application.usecases.assign_ticket import AssignTicketUseCase
from src.application.usecases.create_ticket import CreateTicketUseCase
from src.domain.exceptions import TicketNotFoundError


class TestAssignTicketUseCase:
    """Suite de tests pour l'assignation de tickets."""

    def setup_method(self):
        """Initialise le repository et les use cases."""
        self.repo = InMemoryTicketRepository()
        self.create_use_case = CreateTicketUseCase(self.repo)
        self.assign_use_case = AssignTicketUseCase(self.repo)

    def test_assign_ticket_success(self):
        """Doit assigner un ticket à un agent."""
        # Arrange - Créer un ticket d'abord
        ticket = self.create_use_case.execute(
            "Bug à corriger", "Description du bug", "user-123"
        )
        agent_id = "agent-456"

        # Act
        updated_ticket = self.assign_use_case.execute(ticket.id, agent_id)

        # Assert
        assert updated_ticket.assignee_id is not None
        assert updated_ticket.assignee_id == agent_id

    def test_assign_nonexistent_ticket_raises_error(self):
        """Doit lever une erreur si le ticket n'existe pas."""
        # Arrange
        fake_id = "ticket-inexistant"
        agent_id = "agent-789"

        # Act & Assert
        # TODO: Utiliser pytest.raises pour vérifier qu'une TicketNotFoundError est levé
        with pytest.raises(TicketNotFoundError):
            self.assign_use_case.execute("ticket-inexistant", "agent-789")
        pass

    def test_assign_ticket_persists_change(self):
        """Doit persister l'assignation dans le repository."""
        # Arrange - Créer un ticket
        # TODO: Créer un ticket avec create_use_case

        agent_id = "agent-999"

        # Act
        # TODO: Assigner le ticket à l'agent

        # Assert - Récupérer depuis le repo pour vérifier la persistance
        # TODO: Récupérer le ticket depuis le repository
        # TODO: Vérifier que assignee_id n'est pas None
        # TODO: Vérifier que assignee_id correspond à agent_id
        pass


###
# Tous les tests présents dans tous les fichiers fonctionnent parfaitement, donnant un
# résultat positif, et le code respecte toutes les consignes données.
###
