"""Repository interfaces for item application layer."""

from typing import Protocol
from uuid import UUID

from be_task_ca.item.domain.entities import ItemEntity


class ItemRepositoryInterface(Protocol):
    def save_item(self, item: ItemEntity) -> ItemEntity:
        """Persist an item model and return it."""

    def get_all_items(self) -> list[ItemEntity]:
        """Return all item models."""

    def find_item_by_name(self, name: str) -> ItemEntity | None:
        """Return item model by name, or None if missing."""

    def find_item_by_id(self, item_id: UUID) -> ItemEntity | None:
        """Return item model by id, or None if missing."""


