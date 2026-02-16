from uuid import uuid4

from be_task_ca.item.application.usecases.list_items import ListItemsUseCase
from be_task_ca.item.domain.entities import ItemEntity


class MockItemRepository:
    def __init__(self, items: list[ItemEntity]) -> None:
        self._items = items

    def save_item(self, item: ItemEntity) -> ItemEntity:
        return item

    def get_all_items(self) -> list[ItemEntity]:
        return self._items

    def find_item_by_name(self, name: str) -> ItemEntity | None:
        return None

    def find_item_by_id(self, item_id):
        return None


def test_should_map_repository_items_to_result_dto():
    items = [
        ItemEntity(
            id=uuid4(),
            name="Book",
            description="Paper",
            price=12.5,
            quantity=7,
        )
    ]
    use_case = ListItemsUseCase(MockItemRepository(items))

    result = use_case.execute()

    assert len(result.items) == 1
    assert result.items[0].name == "Book"
    assert result.items[0].quantity == 7
