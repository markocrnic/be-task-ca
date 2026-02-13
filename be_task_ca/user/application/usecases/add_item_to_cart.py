"""Add item to cart use case implementation."""

from be_task_ca.user.application.dto import AddToCartCommand, ListCartItemsResult
from be_task_ca.user.application.exceptions import (
    ItemAlreadyInCartError,
    ItemNotFoundError,
    NotEnoughStockError,
    UserNotFoundError,
)
from be_task_ca.user.application.interfaces.cart_repository_interface import (
    CartRepositoryInterface,
)
from be_task_ca.user.application.interfaces.inventory_gateway_interface import (
    InventoryGatewayInterface,
)
from be_task_ca.user.application.interfaces.user_repository_interface import (
    UserRepositoryInterface,
)
from be_task_ca.user.application.usecases.list_cart_items import ListCartItemsUseCase
from be_task_ca.user.domain.entities import CartItemEntity


class AddItemToCartUseCase:
    """Add an inventory item to user's cart if all checks pass."""

    def __init__(
        self,
        user_repository: UserRepositoryInterface,
        cart_repository: CartRepositoryInterface,
        inventory_gateway: InventoryGatewayInterface,
    ) -> None:
        self._user_repository = user_repository
        self._cart_repository = cart_repository
        self._inventory_gateway = inventory_gateway

    def execute(self, command: AddToCartCommand) -> ListCartItemsResult:
        user = self._user_repository.find_user_by_id(command.user_id)
        if user is None:
            raise UserNotFoundError("User does not exist")

        item = self._inventory_gateway.find_item_by_id(command.item_id)
        if item is None:
            raise ItemNotFoundError("Item does not exist")
        if item.quantity < command.quantity:
            raise NotEnoughStockError("Not enough items in stock")

        existing_cart_items = self._cart_repository.find_cart_items_for_user_id(command.user_id)
        item_ids = [cart_item.item_id for cart_item in existing_cart_items]
        if command.item_id in item_ids:
            raise ItemAlreadyInCartError("Item already in cart")

        self._cart_repository.save_cart_item(
            CartItemEntity(
                user_id=command.user_id,
                item_id=command.item_id,
                quantity=command.quantity,
            )
        )

        return ListCartItemsUseCase(self._cart_repository).execute(command.user_id)
