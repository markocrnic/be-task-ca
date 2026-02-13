"""Interface for accessing inventory data from user/cart use cases."""

from dataclasses import dataclass
from typing import Protocol
from uuid import UUID


@dataclass(frozen=True)
class InventoryItemSnapshot:
    """Minimal inventory data needed by user/cart application logic."""

    id: UUID
    name: str
    description: str | None
    price: float
    quantity: int


class InventoryGatewayInterface(Protocol):
    def find_item_by_id(self, item_id: UUID) -> InventoryItemSnapshot | None:
        """Return inventory item by ID or None."""
