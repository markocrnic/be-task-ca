"""Domain entities for user context."""

from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class UserEntity:
    id: UUID
    email: str
    first_name: str
    last_name: str
    hashed_password: str
    shipping_address: str | None


@dataclass(frozen=True)
class CartItemEntity:
    user_id: UUID
    item_id: UUID
    quantity: int
