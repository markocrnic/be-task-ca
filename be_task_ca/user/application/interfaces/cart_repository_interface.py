"""Repository interface for cart item entities."""

from typing import Protocol
from uuid import UUID

from be_task_ca.user.domain.entities import CartItemEntity


class CartRepositoryInterface(Protocol):
    def find_cart_items_for_user_id(self, user_id: UUID) -> list[CartItemEntity]:
        """Return all cart items for a user."""

    def save_cart_item(self, cart_item: CartItemEntity) -> CartItemEntity:
        """Persist a cart item and return it."""
