from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from be_task_ca.common import get_db
from be_task_ca.user.adapters.api.schema import AddToCartRequest, CreateUserRequest
from be_task_ca.user.adapters.db.cart_repository import SqlAlchemyCartRepository
from be_task_ca.user.adapters.db.inventory_gateway import SqlAlchemyInventoryGateway
from be_task_ca.user.adapters.db.user_repository import SqlAlchemyUserRepository
from be_task_ca.user.application.usecases.add_item_to_cart import AddItemToCartUseCase
from be_task_ca.user.application.usecases.create_user import CreateUserUseCase
from be_task_ca.user.application.usecases.list_cart_items import ListCartItemsUseCase
from be_task_ca.user.adapters.api.handlers import (
    add_item_to_cart,
    create_user,
    list_items_in_cart,
)


user_router = APIRouter(
    prefix="/users",
    tags=["user"],
)


@user_router.post("/")
async def post_customer(user: CreateUserRequest, db: Session = Depends(get_db)):
    use_case = CreateUserUseCase(SqlAlchemyUserRepository(db))
    return create_user(user, use_case)


@user_router.post("/{user_id}/cart")
async def post_cart(
    user_id: UUID, cart_item: AddToCartRequest, db: Session = Depends(get_db)
):
    use_case = AddItemToCartUseCase(
        user_repository=SqlAlchemyUserRepository(db),
        cart_repository=SqlAlchemyCartRepository(db),
        inventory_gateway=SqlAlchemyInventoryGateway(db),
    )
    return add_item_to_cart(user_id, cart_item, use_case)


@user_router.get("/{user_id}/cart")
async def get_cart(user_id: UUID, db: Session = Depends(get_db)):
    use_case = ListCartItemsUseCase(SqlAlchemyCartRepository(db))
    return list_items_in_cart(user_id, use_case)
