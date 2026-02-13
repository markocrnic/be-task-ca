"""SQLAlchemy-backed inventory gateway adapter for user/cart context."""

from uuid import UUID

from sqlalchemy.orm import Session

from be_task_ca.item.model import Item
from be_task_ca.user.application.interfaces.inventory_gateway_interface import (
    InventoryItemSnapshot,
    InventoryGatewayInterface,
)


class SqlAlchemyInventoryGateway(InventoryGatewayInterface):
    """Inventory gateway implementation using local SQLAlchemy session."""

    def __init__(self, db: Session) -> None:
        self._db = db

    def find_item_by_id(self, item_id: UUID) -> InventoryItemSnapshot | None:
        model = self._db.query(Item).filter(Item.id == item_id).first()
        if model is None:
            return None

        return InventoryItemSnapshot(
            id=model.id,
            name=model.name,
            description=model.description,
            price=model.price,
            quantity=model.quantity,
        )
