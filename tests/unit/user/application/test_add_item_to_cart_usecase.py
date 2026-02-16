from uuid import uuid4

import pytest

from be_task_ca.user.application.dto import AddToCartCommand
from be_task_ca.user.application.exceptions import (
    ItemAlreadyInCartError,
    ItemNotFoundError,
    NotEnoughStockError,
    UserNotFoundError,
)
from be_task_ca.user.application.interfaces.inventory_gateway_interface import (
    InventoryItemSnapshot,
)
from be_task_ca.user.application.usecases.add_item_to_cart import AddItemToCartUseCase
from be_task_ca.user.domain.entities import CartItemEntity, UserEntity


class MockUserRepository:
    def __init__(self, user: UserEntity | None) -> None:
        self._user = user

    def save_user(self, user: UserEntity) -> UserEntity:
        return user

    def find_user_by_email(self, email: str) -> UserEntity | None:
        return None

    def find_user_by_id(self, user_id):
        if self._user and self._user.id == user_id:
            return self._user
        return None


class MockCartRepository:
    def __init__(self, existing_items: list[CartItemEntity] | None = None) -> None:
        self._items = existing_items or []
        self.saved_items: list[CartItemEntity] = []

    def find_cart_items_for_user_id(self, user_id):
        return [item for item in self._items if item.user_id == user_id]

    def save_cart_item(self, cart_item: CartItemEntity) -> CartItemEntity:
        self._items.append(cart_item)
        self.saved_items.append(cart_item)
        return cart_item


class MockInventoryGateway:
    def __init__(self, item: InventoryItemSnapshot | None) -> None:
        self._item = item

    def find_item_by_id(self, item_id):
        if self._item and self._item.id == item_id:
            return self._item
        return None


def _build_user() -> UserEntity:
    return UserEntity(
        id=uuid4(),
        email="marko@example.com",
        first_name="Marko",
        last_name="Crnic",
        hashed_password="hash",
        shipping_address="Street 1",
    )


def _build_inventory_item(item_id):
    return InventoryItemSnapshot(
        id=item_id,
        name="Keyboard",
        description="Mechanical",
        price=99.0,
        quantity=5,
    )


def test_should_raise_when_user_does_not_exist():
    use_case = AddItemToCartUseCase(
        user_repository=MockUserRepository(user=None),
        cart_repository=MockCartRepository(),
        inventory_gateway=MockInventoryGateway(item=None),
    )

    with pytest.raises(UserNotFoundError):
        use_case.execute(
            AddToCartCommand(user_id=uuid4(), item_id=uuid4(), quantity=1)
        )


def test_should_raise_when_item_does_not_exist():
    user = _build_user()
    use_case = AddItemToCartUseCase(
        user_repository=MockUserRepository(user=user),
        cart_repository=MockCartRepository(),
        inventory_gateway=MockInventoryGateway(item=None),
    )

    with pytest.raises(ItemNotFoundError):
        use_case.execute(
            AddToCartCommand(user_id=user.id, item_id=uuid4(), quantity=1)
        )


def test_should_raise_when_not_enough_stock():
    user = _build_user()
    item_id = uuid4()
    use_case = AddItemToCartUseCase(
        user_repository=MockUserRepository(user=user),
        cart_repository=MockCartRepository(),
        inventory_gateway=MockInventoryGateway(item=_build_inventory_item(item_id)),
    )

    with pytest.raises(NotEnoughStockError):
        use_case.execute(AddToCartCommand(user_id=user.id, item_id=item_id, quantity=10))


def test_should_raise_when_item_is_already_in_cart():
    user = _build_user()
    item_id = uuid4()
    use_case = AddItemToCartUseCase(
        user_repository=MockUserRepository(user=user),
        cart_repository=MockCartRepository(
            existing_items=[CartItemEntity(user_id=user.id, item_id=item_id, quantity=1)]
        ),
        inventory_gateway=MockInventoryGateway(item=_build_inventory_item(item_id)),
    )

    with pytest.raises(ItemAlreadyInCartError):
        use_case.execute(AddToCartCommand(user_id=user.id, item_id=item_id, quantity=2))


def test_should_save_cart_item_and_return_updated_cart_when_valid_request():
    user = _build_user()
    item_id = uuid4()
    cart_repository = MockCartRepository()
    use_case = AddItemToCartUseCase(
        user_repository=MockUserRepository(user=user),
        cart_repository=cart_repository,
        inventory_gateway=MockInventoryGateway(item=_build_inventory_item(item_id)),
    )

    result = use_case.execute(AddToCartCommand(user_id=user.id, item_id=item_id, quantity=2))

    assert len(cart_repository.saved_items) == 1
    assert len(result.items) == 1
    assert result.items[0].item_id == item_id
    assert result.items[0].quantity == 2
