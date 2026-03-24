"""
Entité Ticket (ticket de support).

TODO (TD01) : Compléter cette classe avec les attributs et méthodes nécessaires.
C'est l'entité centrale du domaine métier.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional

from src.domain.exceptions import (
    InvalidTicketStateError,
    TicketNotAssignedError,
    WrongAgentError,
)
from src.domain.priority import Priority
from src.domain.status import Status


def _now_utc() -> datetime:
    """Retourne l'heure actuelle en UTC."""
    return datetime.now(timezone.utc)


@dataclass
class Ticket:
    """
    Entité principale du domaine : un ticket de support.

    TODO: Compléter cette classe avec :
    1. Les attributs obligatoires (id, title, description, status...)
    2. Les attributs optionnels (assignee, dates...)
    3. Les méthodes métier (assign, close...)

    Pensez aux règles métier (invariants) :
    - Un ticket doit avoir un titre non vide
    - Un ticket fermé ne peut plus être modifié
    - etc.

    Attributs:
        id: Identifiant unique du ticket
        title: Titre court décrivant le problème
        description: Description détaillée
        # TODO: Ajouter les autres attributs
    """

    id: str
    title: str
    description: str
    creator_id: str
    priority: Priority = Priority.MEDIUM
    assignee_id: str = None
    _status: Status = Status.OPEN
    created_at: datetime = field(default_factory=_now_utc)
    updated_at: datetime = field(default_factory=_now_utc)
    started_at: Optional[datetime] = None

    # Transitions autorisées
    ALLOWED_TRANSITIONS = {
        Status.OPEN: [Status.IN_PROGRESS],
        Status.IN_PROGRESS: [Status.RESOLVED],
        Status.RESOLVED: [Status.CLOSED, Status.IN_PROGRESS],
        Status.CLOSED: [Status.IN_PROGRESS],
    }

    def assign(self, user_id: str):
        if self.status == Status.CLOSED:
            raise ValueError("Trying to assign a closed ticket!")
        self.assignee_id = user_id

    def start(self, agent_id: str, started_at: datetime) -> None:
        """
        Démarre le traitement du ticket.

        Validations métier:
        1. Le ticket doit être assigné
        2. L'agent doit être celui assigné
        3. Le ticket doit être en statut OPEN

        Args:
            agent_id: ID de l'agent qui démarre le ticket
            started_at: Date/heure du démarrage

        Raises:
            TicketNotAssignedError: Si le ticket n'est pas assigné
            WrongAgentError: Si agent_id != assignee_id
            InvalidTicketStateError: Si le statut n'est pas OPEN
        """
        # Validation 1 : Ticket doit être assigné
        if self.assignee_id is None:
            raise TicketNotAssignedError("Ticket must be assigned before starting")

        # Validation 2 : L'agent doit être le bon
        if self.assignee_id != agent_id:
            raise WrongAgentError(
                f"Only agent {self.assignee_id} can start this ticket, not {agent_id}"
            )

        # Validation 3 : Le ticket doit être OPEN
        if self._status != Status.OPEN:
            raise InvalidTicketStateError(
                f"Ticket must be OPEN to start, current status: {self._status.value}"
            )

        # Effectuer la transition et enregistrer l'heure de démarrage
        self.transition_to(Status.IN_PROGRESS, started_at)
        self.started_at = started_at

    def __post_init__(self):
        if not self.title.strip():
            raise ValueError("Ticket title cannot be empty.")
        if not self.creator_id.strip():
            raise ValueError("Username cannot be empty.")

    def close(self):
        self.transition_to(
            Status.CLOSED, _now_utc()
        )  # Valide automatiquement la transition
        self.closed_at = _now_utc()

    def resolve(self):
        self.transition_to(Status.RESOLVED, _now_utc())

    def transition_to(self, new_status: Status, updated_at: datetime) -> None:
        """Fait transiter le ticket vers un nouveau statut."""
        if new_status not in self.ALLOWED_TRANSITIONS.get(self._status, []):
            raise ValueError(
                f"Cannot transition from {self._status.value} to {new_status.value}"
            )
        self._status = new_status
        self.updated_at = updated_at

    @property
    def status(self) -> Status:
        return self._status
