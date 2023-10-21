import secrets

from lms.app import app
from tests.factories import UserFactory


def create_admin_user() -> None:
    with app.app_context():
        admin_user = "admin"
        hashed_password = "$2b$12$6I5Ls.Z7UNfYZZHV.ElhJ.qu/.g/2CW3W9VzQPpP.7YdgxYman.2S"
        UserFactory.create(
            username=admin_user,
            first_name=admin_user,
            last_name=admin_user,
            password=hashed_password,
            email="admin@admin.com",
            auth_token=secrets.token_hex(24),
        )


if __name__ == "__main__":
    create_admin_user()
