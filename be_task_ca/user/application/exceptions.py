"""Application-level exceptions for user use cases."""


class UserAlreadyExistsError(Exception):
    """Raised when a user with a given email already exists."""


class UserNotFoundError(Exception):
    """Raised when a user does not exist."""


class ItemNotFoundError(Exception):
    """Raised when an inventory item does not exist."""


class NotEnoughStockError(Exception):
    """Raised when requested item quantity is not available."""


class ItemAlreadyInCartError(Exception):
    """Raised when item is already present in user's cart."""
