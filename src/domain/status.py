from enum import Enum


class Status(Enum):
    """
    États possibles d'un ticket.

    Le cycle de vie typique d'un ticket suit généralement :
    OPEN -> IN_PROGRESS -> RESOLVED -> CLOSED
    """

    OPEN = "open"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"
    CLOSED = "closed"
