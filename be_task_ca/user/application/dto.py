"""Application DTOs for user use cases."""

from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class CreateUserCommand:
    first_name: str
    last_name: str
    email: str
    password: str
    shipping_address: str | None


@dataclass(frozen=True)
class CreateUserResult:
    id: UUID
    first_name: str
    last_name: str
    email: str
    shipping_address: str | None


@dataclass(frozen=True)
class AddToCartCommand:
    user_id: UUID
    item_id: UUID
    quantity: int


@dataclass(frozen=True)
class CartItemResult:
    item_id: UUID
    quantity: int


@dataclass(frozen=True)
class ListCartItemsResult:
    items: list[CartItemResult]
