"""SQLAlchemy-backed item repository adapter."""

from uuid import UUID

from sqlalchemy.orm import Session

from be_task_ca.item.application.interfaces.item_repository_interface import (
    ItemRepositoryInterface,
)
from be_task_ca.item.domain.entities import ItemEntity
from be_task_ca.item.adapters.db.model import Item

from .mappers import to_entity, to_model


class SqlAlchemyItemRepository(ItemRepositoryInterface):
    """SQLAlchemy implementation of item repository interface."""

    def __init__(self, db: Session) -> None:
        self._db = db

    def save_item(self, item: ItemEntity) -> ItemEntity:
        model = to_model(item)
        self._db.add(model)
        self._db.commit()
        return to_entity(model)

    def get_all_items(self) -> list[ItemEntity]:
        models = self._db.query(Item).all()
        return [to_entity(model) for model in models]

    def find_item_by_name(self, name: str) -> ItemEntity | None:
        model = self._db.query(Item).filter(Item.name == name).first()
        if model is None:
            return None

        return to_entity(model)

    def find_item_by_id(self, item_id: UUID) -> ItemEntity | None:
        model = self._db.query(Item).filter(Item.id == item_id).first()
        if model is None:
            return None

        return to_entity(model)
