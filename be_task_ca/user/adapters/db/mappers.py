"""Mapping helpers for user DB adapters."""

from be_task_ca.user.domain.entities import CartItemEntity, UserEntity
from be_task_ca.user.adapters.db.model import CartItem, User


def user_item_model_to_entity(model: User) -> UserEntity:
    """Map SQLAlchemy user model to domain entity."""
    return UserEntity(
        id=model.id,
        email=model.email,
        first_name=model.first_name,
        last_name=model.last_name,
        hashed_password=model.hashed_password,
        shipping_address=model.shipping_address,
    )


def user_item_entity_to_model(entity: UserEntity) -> User:
    """Map domain user entity to SQLAlchemy model."""
    return User(
        email=entity.email,
        first_name=entity.first_name,
        last_name=entity.last_name,
        hashed_password=entity.hashed_password,
        shipping_address=entity.shipping_address,
    )


def cart_item_model_to_entity(model: CartItem) -> CartItemEntity:
    """Map SQLAlchemy cart item model to domain entity."""
    return CartItemEntity(
        user_id=model.user_id,
        item_id=model.item_id,
        quantity=model.quantity,
    )


def cart_item_entity_to_model(entity: CartItemEntity) -> CartItem:
    """Map domain cart item entity to SQLAlchemy model."""
    return CartItem(
        user_id=entity.user_id,
        item_id=entity.item_id,
        quantity=entity.quantity,
    )
