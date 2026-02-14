from fastapi import HTTPException

from be_task_ca.user.adapters.api.schema import (
    AddToCartRequest,
    AddToCartResponse,
    CreateUserRequest,
    CreateUserResponse,
)
from be_task_ca.user.application.dto import (
    AddToCartCommand,
    CreateUserCommand,
    CreateUserResult,
)
from be_task_ca.user.application.exceptions import (
    ItemAlreadyInCartError,
    ItemNotFoundError,
    NotEnoughStockError,
    UserAlreadyExistsError,
    UserNotFoundError,
)
from be_task_ca.user.application.usecases.add_item_to_cart import AddItemToCartUseCase
from be_task_ca.user.application.usecases.create_user import CreateUserUseCase
from be_task_ca.user.application.usecases.list_cart_items import ListCartItemsUseCase


def create_user(create_user: CreateUserRequest, use_case: CreateUserUseCase) -> CreateUserResponse:
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


def list_items_in_cart(user_id, use_case: ListCartItemsUseCase):
    cart_items = use_case.execute(user_id)
    return AddToCartResponse(items=list(map(cart_item_result_to_schema, cart_items.items)))


def cart_item_result_to_schema(result):
    return AddToCartRequest(item_id=result.item_id, quantity=result.quantity)


def add_item_to_cart(
    user_id: int,
    cart_item: AddToCartRequest,
    use_case: AddItemToCartUseCase,
) -> AddToCartResponse:
    command = AddToCartCommand(
        user_id=user_id,
        item_id=cart_item.item_id,
        quantity=cart_item.quantity,
    )

    try:
        result = use_case.execute(command)
    except UserNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except ItemNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except (NotEnoughStockError, ItemAlreadyInCartError) as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc

    return AddToCartResponse(items=list(map(cart_item_result_to_schema, result.items)))
