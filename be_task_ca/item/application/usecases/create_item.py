"""Create item use case implementation."""

from be_task_ca.item.application.dto import CreateItemCommand, CreateItemResult
from be_task_ca.item.application.exceptions import ItemAlreadyExistsError
from be_task_ca.item.application.interfaces.item_repository_interface import (
    ItemRepositoryInterface,
)
from be_task_ca.item.domain.entities import ItemEntity


class CreateItemUseCase:
    """Create an item if no item with the same name exists."""

    def __init__(self, item_repository: ItemRepositoryInterface) -> None:
        self._item_repository = item_repository

    def execute(self, command: CreateItemCommand) -> CreateItemResult:
        existing_item = self._item_repository.find_item_by_name(command.name)
        if existing_item is not None:
            raise ItemAlreadyExistsError("An item with this name already exists")

        new_item = ItemEntity(
            id=None,
            name=command.name,
            description=command.description,
            price=command.price,
            quantity=command.quantity,
        )
        saved_item = self._item_repository.save_item(new_item)

        return CreateItemResult(
            id=saved_item.id,
            name=saved_item.name,
            description=saved_item.description,
            price=saved_item.price,
            quantity=saved_item.quantity,
        )
