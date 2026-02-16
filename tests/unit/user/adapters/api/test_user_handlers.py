from uuid import uuid4

import pytest
from fastapi import HTTPException

from be_task_ca.user.adapters.api.handlers import add_item_to_cart, create_user
from be_task_ca.user.adapters.api.schema import AddToCartRequest, CreateUserRequest
from be_task_ca.user.application.dto import CreateUserResult, ListCartItemsResult, CartItemResult
from be_task_ca.user.application.exceptions import (
    ItemAlreadyInCartError,
    ItemNotFoundError,
    NotEnoughStockError,
    UserAlreadyExistsError,
    UserNotFoundError,
)


class MockCreateUserUseCase:
    def __init__(self, result: CreateUserResult | None = None, error: Exception | None = None):
        self._result = result
        self._error = error

    def execute(self, command):
        if self._error:
            raise self._error
        return self._result


class MockAddItemToCartUseCase:
    def __init__(
        self,
        result: ListCartItemsResult | None = None,
        error: Exception | None = None,
    ):
        self._result = result
        self._error = error

    def execute(self, command):
        if self._error:
            raise self._error
        return self._result


@pytest.mark.parametrize(
    ("error", "status_code"),
    [
        (UserNotFoundError("missing user"), 404),
        (ItemNotFoundError("missing item"), 404),
        (NotEnoughStockError("not enough"), 409),
        (ItemAlreadyInCartError("already in cart"), 409),
    ],
)
def test_should_map_add_to_cart_errors_to_http_status(error: Exception, status_code: int):
    use_case = MockAddItemToCartUseCase(error=error)

    with pytest.raises(HTTPException) as exc_info:
        add_item_to_cart(
            user_id=uuid4(),
            cart_item=AddToCartRequest(item_id=uuid4(), quantity=1),
            use_case=use_case,
        )

    assert exc_info.value.status_code == status_code
    assert exc_info.value.detail == str(error)


def test_should_map_create_user_already_exists_error_to_http_409():
    use_case = MockCreateUserUseCase(error=UserAlreadyExistsError("duplicate user"))

    with pytest.raises(HTTPException) as exc_info:
        create_user(
            CreateUserRequest(
                first_name="Marko",
                last_name="Crnic",
                email="marko@example.com",
                password="pass",
                shipping_address="Street 1",
            ),
            use_case,
        )

    assert exc_info.value.status_code == 409
    assert exc_info.value.detail == "duplicate user"


def test_should_return_create_user_response_when_use_case_succeeds():
    use_case = MockCreateUserUseCase(
        result=CreateUserResult(
            id=uuid4(),
            first_name="Marko",
            last_name="Crnic",
            email="marko@example.com",
            shipping_address="Street 1",
        )
    )

    response = create_user(
        CreateUserRequest(
            first_name="Marko",
            last_name="Crnic",
            email="marko@example.com",
            password="pass",
            shipping_address="Street 1",
        ),
        use_case,
    )

    assert response.email == "marko@example.com"
    assert response.first_name == "Marko"


def test_should_return_add_to_cart_response_when_use_case_succeeds():
    item_id = uuid4()
    use_case = MockAddItemToCartUseCase(
        result=ListCartItemsResult(items=[CartItemResult(item_id=item_id, quantity=2)])
    )

    response = add_item_to_cart(
        user_id=uuid4(),
        cart_item=AddToCartRequest(item_id=item_id, quantity=2),
        use_case=use_case,
    )

    assert len(response.items) == 1
    assert response.items[0].item_id == item_id
    assert response.items[0].quantity == 2
