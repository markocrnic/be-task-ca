"""SQLAlchemy-backed user repository adapter."""

from uuid import UUID

from sqlalchemy.orm import Session

from be_task_ca.user.application.interfaces.user_repository_interface import (
    UserRepositoryInterface,
)
from be_task_ca.user.domain.entities import UserEntity
from be_task_ca.user.adapters.db.model import User

from .mappers import user_item_entity_to_model, user_item_model_to_entity


class SqlAlchemyUserRepository(UserRepositoryInterface):
    """SQLAlchemy implementation of user repository interface."""

    def __init__(self, db: Session) -> None:
        self._db = db

    def save_user(self, user: UserEntity) -> UserEntity:
        model = user_item_entity_to_model(user)
        self._db.add(model)
        self._db.commit()
        return user_item_model_to_entity(model)

    def find_user_by_email(self, email: str) -> UserEntity | None:
        model = self._db.query(User).filter(User.email == email).first()
        if model is None:
            return None
        return user_item_model_to_entity(model)

    def find_user_by_id(self, user_id: UUID) -> UserEntity | None:
        model = self._db.query(User).filter(User.id == user_id).first()
        if model is None:
            return None
        return user_item_model_to_entity(model)
