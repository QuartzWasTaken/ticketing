"""
Use case : Creer un utilisateur.

Ce use case orchestre la creation d'un utilisateur en utilisant les entites du domaine
et le port UserRepository, sans dependre d'une implementation concrete.
"""

import uuid

from src.domain.user import User
from src.ports.user_repository import UserRepository


class CreateUserUseCase:
    """Cas d'usage pour creer un nouvel utilisateur."""

    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def execute(
        self,
        username: str,
        is_agent: bool = False,
        is_admin: bool = False,
    ) -> User:
        """Execute la creation d'un utilisateur."""
        existing_user = self.user_repo.find_by_username(username)
        if existing_user:
            raise ValueError(f"Username '{username}' already exists")

        user_id = str(uuid.uuid4())

        user = User(
            id=user_id,
            username=username,
            is_agent=is_agent,
            is_admin=is_admin,
        )

        self.user_repo.save(user)

        return user
