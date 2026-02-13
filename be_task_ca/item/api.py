from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from be_task_ca.item.adapters.db.repository import SqlAlchemyItemRepository
from be_task_ca.item.application.usecases.create_item import CreateItemUseCase
from be_task_ca.item.application.usecases.list_items import ListItemsUseCase

from .usecases import create_item, get_all

from ..common import get_db

from .schema import CreateItemRequest, CreateItemResponse


item_router = APIRouter(
    prefix="/items",
    tags=["item"],
)


@item_router.post("/")
async def post_item(
    item: CreateItemRequest, db: Session = Depends(get_db)
) -> CreateItemResponse:
    use_case = CreateItemUseCase(SqlAlchemyItemRepository(db))
    return create_item(item, use_case)


@item_router.get("/")
async def get_items(db: Session = Depends(get_db)):
    use_case = ListItemsUseCase(SqlAlchemyItemRepository(db))
    return get_all(use_case)
