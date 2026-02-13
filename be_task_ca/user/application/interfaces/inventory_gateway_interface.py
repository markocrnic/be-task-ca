"""Interface for accessing inventory data from user/cart use cases."""

from typing import Protocol
from uuid import UUID

from be_task_ca.item.domain.entities import ItemEntity


class InventoryGatewayInterface(Protocol):
    def find_item_by_id(self, item_id: UUID) -> ItemEntity | None:
        """Return inventory item by ID or None."""
