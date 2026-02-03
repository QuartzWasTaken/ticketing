"""
Entité Ticket (ticket de support).

TODO (TD01) : Compléter cette classe avec les attributs et méthodes nécessaires.
C'est l'entité centrale du domaine métier.
"""

from dataclasses import dataclass
from datetime import datetime, timezone

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
    priority: Priority
    assignee_id: str = None
    _status: Status = Status.OPEN
    created_at: datetime = _now_utc()
    updated_at: datetime = _now_utc()

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
        self.transition_to(Status.IN_PROGRESS, _now_utc())
        self.assignee_id = user_id

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

    def start(self):
        self.transition_to(Status.IN_PROGRESS, _now_utc())

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
