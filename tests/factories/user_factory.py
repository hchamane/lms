import factory

from lms.domains import User, UserRole

from .base import BaseFactory


class UserFactory(BaseFactory):
    class Meta:
        model = User

    username = factory.Faker("name")
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    email = factory.Faker("email")
    password = factory.Faker("password")
    role_id = UserRole.ADMIN.value
