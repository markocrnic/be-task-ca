"""Create user use case implementation."""

import hashlib

from be_task_ca.user.application.dto import CreateUserCommand, CreateUserResult
from be_task_ca.user.application.exceptions import UserAlreadyExistsError
from be_task_ca.user.application.interfaces.user_repository_interface import (
    UserRepositoryInterface,
)
from be_task_ca.user.domain.entities import UserEntity


class CreateUserUseCase:
    """Create a user if email is not already registered."""

    def __init__(self, user_repository: UserRepositoryInterface) -> None:
        self._user_repository = user_repository

    def execute(self, command: CreateUserCommand) -> CreateUserResult:
        existing_user = self._user_repository.find_user_by_email(command.email)
        if existing_user is not None:
            raise UserAlreadyExistsError("An user with this email adress already exists")

        new_user = UserEntity(
            id=None,
            first_name=command.first_name,
            last_name=command.last_name,
            email=command.email,
            hashed_password=hashlib.sha512(command.password.encode("UTF-8")).hexdigest(),
            shipping_address=command.shipping_address,
        )
        saved_user = self._user_repository.save_user(new_user)

        return CreateUserResult(
            id=saved_user.id,
            first_name=saved_user.first_name,
            last_name=saved_user.last_name,
            email=saved_user.email,
            shipping_address=saved_user.shipping_address,
        )
