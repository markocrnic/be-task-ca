import hashlib
from uuid import uuid4

import pytest

from be_task_ca.user.application.dto import CreateUserCommand
from be_task_ca.user.application.exceptions import UserAlreadyExistsError
from be_task_ca.user.application.usecases.create_user import CreateUserUseCase
from be_task_ca.user.domain.entities import UserEntity


class MockUserRepository:
    def __init__(self, existing_user: UserEntity | None = None) -> None:
        self._existing_user = existing_user
        self.saved_users: list[UserEntity] = []

    def save_user(self, user: UserEntity) -> UserEntity:
        saved_user = UserEntity(
            id=uuid4(),
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
            hashed_password=user.hashed_password,
            shipping_address=user.shipping_address,
        )
        self.saved_users.append(saved_user)
        return saved_user

    def find_user_by_email(self, email: str) -> UserEntity | None:
        if self._existing_user and self._existing_user.email == email:
            return self._existing_user
        return None

    def find_user_by_id(self, user_id):
        return None


def test_should_create_user_and_hash_password_when_email_is_unique():
    repository = MockUserRepository(existing_user=None)
    use_case = CreateUserUseCase(repository)

    result = use_case.execute(
        CreateUserCommand(
            first_name="Marko",
            last_name="Crnic",
            email="marko@example.com",
            password="secret-password",
            shipping_address="Street 1",
        )
    )

    assert result.email == "marko@example.com"
    assert len(repository.saved_users) == 1
    assert repository.saved_users[0].hashed_password != "secret-password"
    assert repository.saved_users[0].hashed_password == hashlib.sha512(
        "secret-password".encode("UTF-8")
    ).hexdigest()


def test_should_raise_when_user_email_already_exists():
    repository = MockUserRepository(
        existing_user=UserEntity(
            id=uuid4(),
            email="marko@example.com",
            first_name="Existing",
            last_name="User",
            hashed_password="hashed",
            shipping_address="Street 2",
        )
    )
    use_case = CreateUserUseCase(repository)

    with pytest.raises(UserAlreadyExistsError):
        use_case.execute(
            CreateUserCommand(
                first_name="Marko",
                last_name="Crnic",
                email="marko@example.com",
                password="another-pass",
                shipping_address="Street 3",
            )
        )
