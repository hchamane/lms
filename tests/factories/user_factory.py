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
    auth_token = factory.Faker("password")


class TeacherFactory(BaseFactory):
    class Meta:
        model = User

    username = factory.Faker("name")
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    email = factory.Faker("email")
    password = factory.Faker("password")
    role_id = UserRole.TEACHER.value
    auth_token = factory.Faker("password")


class StudentFactory(BaseFactory):
    class Meta:
        model = User

    username = factory.Faker("name")
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    email = factory.Faker("email")
    password = factory.Faker("password")
    role_id = UserRole.STUDENT.value
    auth_token = factory.Faker("password")
