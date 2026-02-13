"""List items use case implementation."""

from be_task_ca.item.application.dto import CreateItemResult, ListItemsResult
from be_task_ca.item.application.interfaces.item_repository_interface import (
    ItemRepositoryInterface,
)


class ListItemsUseCase:
    """Return all items."""

    def __init__(self, item_repository: ItemRepositoryInterface) -> None:
        self._item_repository = item_repository

    def execute(self) -> ListItemsResult:
        items = self._item_repository.get_all_items()
        return ListItemsResult(
            items=[
                CreateItemResult(
                    id=item.id,
                    name=item.name,
                    description=item.description,
                    price=item.price,
                    quantity=item.quantity,
                )
                for item in items
            ]
        )
