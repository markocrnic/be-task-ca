"""Mapping helpers for item DB adapter."""

from be_task_ca.item.domain.entities import ItemEntity
from be_task_ca.item.adapters.db.model import Item


def to_entity(model: Item) -> ItemEntity:
    """Map SQLAlchemy model to domain entity."""
    return ItemEntity(
        id=model.id,
        name=model.name,
        description=model.description,
        price=model.price,
        quantity=model.quantity,
    )


def to_model(entity: ItemEntity) -> Item:
    """Map domain entity to SQLAlchemy model."""
    return Item(
        name=entity.name,
        description=entity.description,
        price=entity.price,
        quantity=entity.quantity,
    )
