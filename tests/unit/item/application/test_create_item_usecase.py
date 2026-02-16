from uuid import uuid4

import pytest

from be_task_ca.item.application.dto import CreateItemCommand
from be_task_ca.item.application.exceptions import ItemAlreadyExistsError
from be_task_ca.item.application.usecases.create_item import CreateItemUseCase
from be_task_ca.item.domain.entities import ItemEntity


class MockItemRepository:
    def __init__(self, existing_item: ItemEntity | None = None) -> None:
        self._existing_item = existing_item
        self.saved_items: list[ItemEntity] = []

    def save_item(self, item: ItemEntity) -> ItemEntity:
        saved_item = ItemEntity(
            id=uuid4(),
            name=item.name,
            description=item.description,
            price=item.price,
            quantity=item.quantity,
        )
        self.saved_items.append(saved_item)
        return saved_item

    def get_all_items(self) -> list[ItemEntity]:
        return self.saved_items

    def find_item_by_name(self, name: str) -> ItemEntity | None:
        if self._existing_item and self._existing_item.name == name:
            return self._existing_item
        return None

    def find_item_by_id(self, item_id):
        return None


def test_should_create_item_when_name_is_unique():
    repository = MockItemRepository(existing_item=None)
    use_case = CreateItemUseCase(repository)

    result = use_case.execute(
        CreateItemCommand(
            name="Book",
            description="Clean Architecture",
            price=19.99,
            quantity=3,
        )
    )

    assert result.name == "Book"
    assert result.quantity == 3
    assert len(repository.saved_items) == 1


def test_should_raise_when_item_name_already_exists():
    repository = MockItemRepository(
        existing_item=ItemEntity(
            id=uuid4(),
            name="Book",
            description="Existing",
            price=10.0,
            quantity=1,
        )
    )
    use_case = CreateItemUseCase(repository)

    with pytest.raises(ItemAlreadyExistsError):
        use_case.execute(
            CreateItemCommand(
                name="Book",
                description="Duplicate",
                price=25.0,
                quantity=5,
            )
        )
