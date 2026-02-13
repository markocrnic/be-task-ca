"""List user cart items use case implementation."""

from uuid import UUID

from be_task_ca.user.application.dto import CartItemResult, ListCartItemsResult
from be_task_ca.user.application.interfaces.cart_repository_interface import (
    CartRepositoryInterface,
)


class ListCartItemsUseCase:
    """Return all cart items for a user."""

    def __init__(self, cart_repository: CartRepositoryInterface) -> None:
        self._cart_repository = cart_repository

    def execute(self, user_id: UUID) -> ListCartItemsResult:
        cart_items = self._cart_repository.find_cart_items_for_user_id(user_id)
        return ListCartItemsResult(
            items=[
                CartItemResult(item_id=item.item_id, quantity=item.quantity)
                for item in cart_items
            ]
        )
