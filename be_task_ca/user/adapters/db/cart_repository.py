"""SQLAlchemy-backed cart repository adapter."""

from uuid import UUID

from sqlalchemy.orm import Session

from be_task_ca.user.application.interfaces.cart_repository_interface import (
    CartRepositoryInterface,
)
from be_task_ca.user.domain.entities import CartItemEntity
from be_task_ca.user.adapters.db.model import CartItem

from .mappers import cart_item_entity_to_model, cart_item_model_to_entity


class SqlAlchemyCartRepository(CartRepositoryInterface):
    """SQLAlchemy implementation of cart repository interface."""

    def __init__(self, db: Session) -> None:
        self._db = db

    def find_cart_items_for_user_id(self, user_id: UUID) -> list[CartItemEntity]:
        models = self._db.query(CartItem).filter(CartItem.user_id == user_id).all()
        return [cart_item_model_to_entity(model) for model in models]

    def save_cart_item(self, cart_item: CartItemEntity) -> CartItemEntity:
        model = cart_item_entity_to_model(cart_item)
        self._db.add(model)
        self._db.commit()
        return cart_item_model_to_entity(model)
