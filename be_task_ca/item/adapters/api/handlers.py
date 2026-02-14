from fastapi import HTTPException

from be_task_ca.item.adapters.api.schema import (
    AllItemsRepsonse,
    CreateItemRequest,
    CreateItemResponse,
)
from be_task_ca.item.application.dto import CreateItemCommand, CreateItemResult
from be_task_ca.item.application.exceptions import ItemAlreadyExistsError
from be_task_ca.item.application.usecases.create_item import CreateItemUseCase
from be_task_ca.item.application.usecases.list_items import ListItemsUseCase


def create_item(item: CreateItemRequest, use_case: CreateItemUseCase) -> CreateItemResponse:
    command = CreateItemCommand(
        name=item.name,
        description=item.description,
        price=item.price,
        quantity=item.quantity,
    )

    try:
        result = use_case.execute(command)
    except ItemAlreadyExistsError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc

    return result_to_schema(result)


def get_all(use_case: ListItemsUseCase):
    item_list = use_case.execute()
    return AllItemsRepsonse(items=list(map(result_to_schema, item_list.items)))


def result_to_schema(item: CreateItemResult) -> CreateItemResponse:
    return CreateItemResponse(
        id=item.id,
        name=item.name,
        description=item.description,
        price=item.price,
        quantity=item.quantity,
    )
