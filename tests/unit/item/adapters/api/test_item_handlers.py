from uuid import uuid4

import pytest
from fastapi import HTTPException

from be_task_ca.item.adapters.api.handlers import create_item, get_all
from be_task_ca.item.adapters.api.schema import CreateItemRequest
from be_task_ca.item.application.dto import CreateItemResult, ListItemsResult
from be_task_ca.item.application.exceptions import ItemAlreadyExistsError


class MockCreateItemUseCase:
    def __init__(self, result: CreateItemResult | None = None, error: Exception | None = None):
        self._result = result
        self._error = error

    def execute(self, command):
        if self._error:
            raise self._error
        return self._result


class MockListItemsUseCase:
    def __init__(self, result: ListItemsResult):
        self._result = result

    def execute(self):
        return self._result


def test_should_map_item_already_exists_error_to_http_409():
    use_case = MockCreateItemUseCase(error=ItemAlreadyExistsError("duplicate"))

    with pytest.raises(HTTPException) as exc_info:
        create_item(
            CreateItemRequest(
                name="Book",
                description="Desc",
                price=10.0,
                quantity=1,
            ),
            use_case,
        )

    assert exc_info.value.status_code == 409
    assert exc_info.value.detail == "duplicate"


def test_should_return_create_item_response_when_use_case_succeeds():
    use_case = MockCreateItemUseCase(
        result=CreateItemResult(
            id=uuid4(),
            name="Book",
            description="Desc",
            price=10.0,
            quantity=1,
        )
    )

    response = create_item(
        CreateItemRequest(name="Book", description="Desc", price=10.0, quantity=1),
        use_case,
    )

    assert response.name == "Book"
    assert response.quantity == 1


def test_should_return_all_items_response_when_listing_items():
    use_case = MockListItemsUseCase(
        result=ListItemsResult(
            items=[
                CreateItemResult(
                    id=uuid4(),
                    name="Keyboard",
                    description="Mechanical",
                    price=99.0,
                    quantity=5,
                )
            ]
        )
    )

    response = get_all(use_case)

    assert len(response.items) == 1
    assert response.items[0].name == "Keyboard"
