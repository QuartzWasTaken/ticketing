"""Tests use cases avec SQLiteTicketRepository (interchangeable avec InMemory)."""

from datetime import datetime, timezone

from src.adapters.clock.fixed_clock import FixedClock
from src.application.usecases.assign_ticket import AssignTicketUseCase
from src.application.usecases.create_ticket import CreateTicketUseCase
from src.application.usecases.start_ticket import StartTicketUseCase
from src.domain.status import Status


class TestSQLiteTicketRepositoryWithUseCases:
    """Valide l'interchangeabilite de l'adaptateur SQLite."""

    def test_create_ticket_with_sqlite(self, sqlite_ticket_repo):
        """CreateTicket fonctionne sans modifier le use case."""
        use_case = CreateTicketUseCase(ticket_repo=sqlite_ticket_repo)

        ticket = use_case.execute(
            title="Bug critique",
            description="Le systeme plante",
            creator_id="user-123",
        )

        assert ticket.id is not None
        assert ticket.status == Status.OPEN

        retrieved = sqlite_ticket_repo.get_by_id(ticket.id)
        assert retrieved is not None
        assert retrieved.title == "Bug critique"

    def test_create_multiple_tickets_with_sqlite(self, sqlite_ticket_repo):
        """Plusieurs tickets sont sauvegardes et recuperables via list_all."""
        use_case = CreateTicketUseCase(ticket_repo=sqlite_ticket_repo)

        first = use_case.execute("Bug 1", "Description 1", "user-1")
        second = use_case.execute("Bug 2", "Description 2", "user-2")

        tickets = sqlite_ticket_repo.list_all()
        ids = {ticket.id for ticket in tickets}

        assert len(tickets) == 2
        assert first.id in ids
        assert second.id in ids

    def test_assign_ticket_persists_with_sqlite(self, sqlite_ticket_repo):
        """AssignTicket persiste bien l'agent assigne en base SQLite."""
        create_use_case = CreateTicketUseCase(ticket_repo=sqlite_ticket_repo)
        assign_use_case = AssignTicketUseCase(ticket_repo=sqlite_ticket_repo)

        ticket = create_use_case.execute(
            title="Bug a corriger",
            description="Description du bug",
            creator_id="user-123",
        )
        updated = assign_use_case.execute(ticket.id, "agent-999")

        assert updated.assignee_id == "agent-999"

        persisted = sqlite_ticket_repo.get_by_id(ticket.id)
        assert persisted is not None
        assert persisted.assignee_id == "agent-999"

    def test_start_ticket_persists_with_sqlite(self, sqlite_ticket_repo):
        """StartTicket fonctionne identiquement avec SQLite et conserve started_at."""
        fixed_time = datetime(2026, 1, 16, 14, 30, 0, tzinfo=timezone.utc)

        create_use_case = CreateTicketUseCase(ticket_repo=sqlite_ticket_repo)
        assign_use_case = AssignTicketUseCase(ticket_repo=sqlite_ticket_repo)
        start_use_case = StartTicketUseCase(
            ticket_repo=sqlite_ticket_repo,
            clock=FixedClock(fixed_time),
        )

        ticket = create_use_case.execute("Bug", "Description", "user-123")
        assign_use_case.execute(ticket.id, "agent-456")

        started = start_use_case.execute(ticket.id, "agent-456")

        assert started.status == Status.IN_PROGRESS
        assert started.started_at == fixed_time

        persisted = sqlite_ticket_repo.get_by_id(ticket.id)
        assert persisted is not None
        assert persisted.status == Status.IN_PROGRESS
        assert persisted.started_at == fixed_time
