"""Application-level exceptions for user use cases."""


class UserAlreadyExistsError(Exception):
    """Raised when a user with a given email already exists."""
