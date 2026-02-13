"""Application-level exceptions for item use cases."""


class ItemAlreadyExistsError(Exception):
    """Raised when an item with the same name already exists."""
