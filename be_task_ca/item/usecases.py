from fastapi import HTTPException
from sqlalchemy.orm import Session

from be_task_ca.item.adapters.db.repository import SqlAlchemyItemRepository
from be_task_ca.item.application.dto import CreateItemCommand, CreateItemResult
from be_task_ca.item.application.exceptions import ItemAlreadyExistsError
from be_task_ca.item.application.usecases.create_item import CreateItemUseCase
from be_task_ca.item.application.usecases.list_items import ListItemsUseCase
from .schema import AllItemsRepsonse, CreateItemRequest, CreateItemResponse


def create_item(item: CreateItemRequest, db: Session) -> CreateItemResponse:
    repository = SqlAlchemyItemRepository(db)
    use_case = CreateItemUseCase(repository)

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


def get_all(db: Session):
    repository = SqlAlchemyItemRepository(db)
    use_case = ListItemsUseCase(repository)
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


def model_to_schema(item) -> CreateItemResponse:
    """Backward-compatible alias kept temporarily during migration."""
    return result_to_schema(item)
