"""
Tests unitaires pour le domaine (TD1).

Ces tests vérifient le comportement des entités du domaine.
Ils doivent passer sans aucune dépendance externe (pas de DB, pas d'API).

Écrivez vos tests ici après avoir implémenté les classes dans src/domain/.
Lancez-les avec : pytest tests/domain/
"""

# TODO (TD1): Décommenter ces imports une fois les classes implémentées
import pytest

from src.domain.status import Status
from src.domain.ticket import Ticket, _now_utc
from src.domain.user import User

# ==========================================================================
# EXEMPLES DE TESTS À ÉCRIRE (décommentez et adaptez)
# ==========================================================================


def test_status_values_exist():
    """Vérifie que les 4 statuts existent."""
    assert Status.OPEN.value == "open"
    assert Status.IN_PROGRESS.value == "in_progress"
    assert Status.RESOLVED.value == "resolved"
    assert Status.CLOSED.value == "closed"


def test_user_creation():
    """Vérifie la création d'un utilisateur."""
    user = User(id="u1", username="alice")
    assert user.id == "u1"
    assert user.username == "alice"


def test_ticket_creation():
    """Vérifie la création d'un ticket avec valeurs par défaut."""
    ticket = Ticket(
        id="t1",
        title="Bug connexion",
        description="Impossible de se connecter",
        creator_id="user1",
    )
    assert ticket.status == Status.OPEN
    assert ticket.assignee_id is None


def test_ticket_assign():
    """Vérifie l'assignation d'un ticket."""
    ticket = Ticket(id="t1", title="Test", description="desc", creator_id="u1")
    ticket.assign("agent1")
    assert ticket.assignee_id == "agent1"


# def test_ticket_close():
#     """Vérifie la fermeture d'un ticket."""
#     ticket = Ticket(id="t1", title="Test", description="desc", creator_id="u1")
#     ticket.close(_now_utc())
#     assert ticket.status == Status.CLOSED


# ==========================================================================
# TESTS DES RÈGLES MÉTIER (invariants) - à vous de les écrire !
# ==========================================================================


def test_cannot_assign_closed_ticket():
    """Règle : Un ticket fermé ne peut plus être assigné."""
    ticket = Ticket(id="t1", title="Test", description="desc", creator_id="u1")
    ticket.start()

    assert ticket.status == Status.IN_PROGRESS

    ticket.resolve()

    ticket.close()

    with pytest.raises(ValueError):
        ticket.assign("JeanMichelNomTresLongPourPouvoirAssign")


def test_cannot_close_already_closed_ticket():
    """Règle : Un ticket déjà fermé ne peut pas être re-fermé."""
    ticket = Ticket(id="t1", title="Test", description="desc", creator_id="u1")
    ticket.start()
    ticket.resolve()
    ticket.close()

    with pytest.raises(ValueError):
        ticket.close()


def test_ticket_title_cannot_be_empty():
    """Règle : Un ticket doit avoir un titre non vide."""
    with pytest.raises(ValueError):
        ticket = Ticket(id="t1", title="", description="desc", creator_id="u1")


def test_ticket_title_cannot_be_all_spaces():
    """Règle : Un ticket doit avoir un titre qui ne soit pas que des espaces."""
    with pytest.raises(ValueError):
        ticket = Ticket(
            id="t1",
            title="                          ",
            description="desc",
            creator_id="u1",
        )


def test_ticket_username_cannot_be_empty():
    """Règle : Un ticket doit avoir un titre non vide."""
    with pytest.raises(ValueError):
        ticket = Ticket(id="t1", title="Test Title", description="desc", creator_id="")


def test_ticket_cannot_modify_closed_ticket_status_by_reassigning():
    """Règle : Un ticket doit avoir un titre non vide."""
    ticket = Ticket(id="t1", title="Test", description="desc", creator_id="u1")
    ticket.start()
    ticket.resolve()
    ticket.close()

    with pytest.raises(ValueError):
        ticket.assign("Zebi")


def test_ticket_respects_given_order():
    """Règle : Un ticket doit avoir un titre non vide."""
    ticket = Ticket(id="t1", title="Test", description="desc", creator_id="u1")
    ticket.start()
    ticket.resolve()
    ticket.close()
    ticket.transition_to(Status.IN_PROGRESS, _now_utc())
    ticket.resolve()
    ticket.transition_to(Status.IN_PROGRESS, _now_utc())


def test_ticket_cannot_go_from_open_to_resolved():
    ticket = Ticket(id="t1", title="Test", description="desc", creator_id="u1")
    with pytest.raises(ValueError):
        ticket.resolve()


def test_ticket_cannot_be_assigned_without_agent_id():
    ticket = Ticket(id="t1", title="Test", description="desc", creator_id="u1")
    with pytest.raises(TypeError):
        ticket.assign()


def test_ticket_cannot_be_created_without_the_creator():
    with pytest.raises(TypeError):
        ticket = Ticket(id="t1", title="Test", description="desc")


def test_ticket_cannot_assign_unknown_statuses():
    ticket = Ticket(id="t1", title="Test", description="desc", creator_id="u1")
    with pytest.raises(AttributeError):
        ticket.transition_to("TEST", _now_utc())
