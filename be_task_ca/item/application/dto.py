"""Application DTOs for item use cases."""

from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class CreateItemCommand:
    name: str
    description: str | None
    price: float
    quantity: int


@dataclass(frozen=True)
class CreateItemResult:
    id: UUID
    name: str
    description: str | None
    price: float
    quantity: int


@dataclass(frozen=True)
class ListItemsResult:
    items: list[CreateItemResult]
