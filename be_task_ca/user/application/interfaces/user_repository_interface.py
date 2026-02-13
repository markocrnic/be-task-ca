"""Repository interface for user entities."""

from typing import Protocol
from uuid import UUID

from be_task_ca.user.domain.entities import UserEntity


class UserRepositoryInterface(Protocol):
    def save_user(self, user: UserEntity) -> UserEntity:
        """Persist a user and return it."""

    def find_user_by_email(self, email: str) -> UserEntity | None:
        """Return user by email or None."""

    def find_user_by_id(self, user_id: UUID) -> UserEntity | None:
        """Return user by ID or None."""
