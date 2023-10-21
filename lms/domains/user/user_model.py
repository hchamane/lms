import enum

from dataclasses import dataclass

from sqlalchemy.exc import IntegrityError

from lms.adapters import BaseMixin, db


class UserRole(enum.Enum):
    ADMIN = 1
    TEATCHER = 2
    STUDENT = 3


@dataclass
class User(BaseMixin, db.Model):
    __tablename__ = "users"

    username: str = db.Column(db.String, unique=True, nullable=False)
    password: str = db.Column(db.String, nullable=False)
    role_id: int = db.Column(db.Integer, nullable=False)
    first_name: str = db.Column(db.String, nullable=False)
    last_name: str = db.Column(db.String, nullable=False)
    email: str = db.Column(db.String, unique=True, nullable=False)
    auth_token: str = db.Column(db.String(255), unique=True)

    def __init__(
        self,
        username: str,
        password: str,
        role_id: int,
        first_name: str,
        last_name: str,
        email: str,
        auth_token: str,
    ) -> None:
        self.username = username
        self.password = password
        self.role_id = role_id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.auth_token = auth_token

    @classmethod
    def create(
        cls, username: str, password: str, role_id: int, first_name: str, last_name: str, email: str, auth_token: str
    ) -> "User":
        user = cls(
            username=username,
            password=password,
            role_id=role_id,
            first_name=first_name,
            last_name=last_name,
            email=email,
            auth_token=auth_token,
        )
        db.session.add(user)
        db.session.commit()
        return user

    def update(self, update_params: dict) -> "User":
        self.username = update_params.get("username", self.username)
        self.role_id = update_params.get("role_id", self.role_id)
        self.first_name = update_params.get("first_name", self.first_name)
        self.last_name = update_params.get("last_name", self.last_name)
        self.email = update_params.get("email", self.email)

        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            raise ValueError("Invalid params")

        return self
