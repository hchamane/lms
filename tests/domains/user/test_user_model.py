import pytest

from lms.domains import User
from tests.factories import UserFactory


@pytest.mark.usefixtures("wipe_users_table")
class TestUserModel:
    def test_user_init(self) -> None:
        user = UserFactory.build()
        assert isinstance(user, User)
        assert isinstance(user.first_name, str)
        assert isinstance(user.last_name, str)
        assert isinstance(user.email, str)
        assert isinstance(user.role_id, int)

    def test_user_init_with_missing_value(self) -> None:
        with pytest.raises(TypeError) as error:
            User()
        assert str(error.value) == (
            "__init__() missing 6 required positional arguments: 'username', 'password',"
            " 'role_id', 'first_name', 'last_name', and 'email'"
        )

    def test_user_create(self) -> None:
        user = UserFactory.build()
        created_user = User.create(
            username=user.username,
            password=user.password,
            role_id=1,
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
        )

        assert isinstance(created_user, User)
        assert created_user.first_name == user.first_name
        assert created_user.last_name == user.last_name
        assert created_user.email == user.email

    def test_user_update(self) -> None:
        user = UserFactory.create()
        updated_user = user.update({"first_name": "updated name"})
        assert isinstance(updated_user, User)
        assert updated_user.first_name == "updated name"

    def test_user_update_if_email_already_exists_rollback(self) -> None:
        user = UserFactory.create()
        another_user = UserFactory.create()

        with pytest.raises(ValueError):
            another_user.update({"email": user.email})
