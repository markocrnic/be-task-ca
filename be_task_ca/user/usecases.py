from fastapi import HTTPException
from sqlalchemy.orm import Session

from be_task_ca.user.adapters.db.cart_repository import SqlAlchemyCartRepository
from be_task_ca.user.adapters.db.user_repository import SqlAlchemyUserRepository
from be_task_ca.user.application.dto import CreateUserCommand, CreateUserResult
from be_task_ca.user.application.exceptions import UserAlreadyExistsError
from be_task_ca.user.application.usecases.create_user import CreateUserUseCase
from be_task_ca.user.application.usecases.list_cart_items import ListCartItemsUseCase

from ..item.model import Item

from ..item.repository import find_item_by_id

from .model import CartItem, User

from .repository import (
    find_user_by_id,
    save_user,
)
from .schema import (
    AddToCartRequest,
    AddToCartResponse,
    CreateUserRequest,
    CreateUserResponse,
)


def create_user(create_user: CreateUserRequest, db: Session) -> CreateUserResponse:
    repository = SqlAlchemyUserRepository(db)
    use_case = CreateUserUseCase(repository)

    command = CreateUserCommand(
        first_name=create_user.first_name,
        last_name=create_user.last_name,
        email=create_user.email,
        password=create_user.password,
        shipping_address=create_user.shipping_address,
    )

    try:
        result = use_case.execute(command)
    except UserAlreadyExistsError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc

    return result_to_create_user_schema(result)


def result_to_create_user_schema(result: CreateUserResult) -> CreateUserResponse:
    return CreateUserResponse(
        id=result.id,
        first_name=result.first_name,
        last_name=result.last_name,
        email=result.email,
        shipping_address=result.shipping_address,
    )


def list_items_in_cart(user_id, db):
    repository = SqlAlchemyCartRepository(db)
    use_case = ListCartItemsUseCase(repository)
    cart_items = use_case.execute(user_id)
    return AddToCartResponse(items=list(map(cart_item_result_to_schema, cart_items.items)))


def cart_item_result_to_schema(result):
    return AddToCartRequest(item_id=result.item_id, quantity=result.quantity)


def cart_item_model_to_schema(model: CartItem):
    """Backward-compatible alias kept temporarily during migration."""
    return AddToCartRequest(item_id=model.item_id, quantity=model.quantity)


def add_item_to_cart(user_id: int, cart_item: AddToCartRequest, db: Session) -> AddToCartResponse:
    user: User = find_user_by_id(user_id, db)
    if user is None:
        raise HTTPException(status_code=404, detail="User does not exist")

    item: Item = find_item_by_id(cart_item.item_id, db)
    if item is None:
        raise HTTPException(status_code=404, detail="Item does not exist")
    if item.quantity < cart_item.quantity:
        raise HTTPException(status_code=409, detail="Not enough items in stock")

    item_ids = [o.item_id for o in user.cart_items]
    if cart_item.item_id in item_ids:
        raise HTTPException(status_code=409, detail="Item already in cart")

    new_cart_item: CartItem = CartItem(
        user_id=user.id, item_id=cart_item.item_id, quantity=cart_item.quantity
    )

    user.cart_items.append(new_cart_item)

    save_user(user, db)

    return list_items_in_cart(user.id, db)
