"""Domain entities for item context."""

from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class ItemEntity:
    id: UUID | None
    name: str
    description: str | None
    price: float
    quantity: int
