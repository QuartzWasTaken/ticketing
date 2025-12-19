from dataclasses import dataclass


@dataclass
class User:
    """
    Représente un utilisateur du système de ticketing.

    TODO: Définir les attributs nécessaires.
    Réfléchissez aux informations minimales pour identifier un utilisateur
    et distinguer ses rôles (simple utilisateur, agent support, admin...).

    Attributes:
        id: Identifiant unique de l'utilisateur
        # TODO: Ajouter d'autres attributs
    """

    id: str
    username: str
    is_agent: bool = False
    is_admin: bool = False

    def __post_init__(self):
        if not self.username:
            raise ValueError("Username cannot be empty.")
