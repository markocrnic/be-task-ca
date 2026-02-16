from uuid import uuid4

from be_task_ca.user.application.usecases.list_cart_items import ListCartItemsUseCase
from be_task_ca.user.domain.entities import CartItemEntity


class MockCartRepository:
    def __init__(self, items: list[CartItemEntity]) -> None:
        self._items = items

    def find_cart_items_for_user_id(self, user_id):
        return [item for item in self._items if item.user_id == user_id]

    def save_cart_item(self, cart_item: CartItemEntity) -> CartItemEntity:
        return cart_item


def test_should_map_cart_entities_to_result_dto():
    user_id = uuid4()
    use_case = ListCartItemsUseCase(
        MockCartRepository(
            items=[
                CartItemEntity(user_id=user_id, item_id=uuid4(), quantity=2),
                CartItemEntity(user_id=uuid4(), item_id=uuid4(), quantity=5),
            ]
        )
    )

    result = use_case.execute(user_id)

    assert len(result.items) == 1
    assert result.items[0].quantity == 2
