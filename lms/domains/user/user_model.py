import enum

from lms.adapters import BaseMixin, db


class UserRole(enum.Enum):
    ADMIN = 1
    TEATCHER = 2
    STUDENT = 3


class User(BaseMixin, db.Model):
    __tablename__ = "users"

    username: str = db.Column(db.String, unique=True, nullable=False)
    password: str = db.Column(db.String, nullable=False)
    role_id: int = db.Column(db.Integer, nullable=False)
    first_name: str = db.Column(db.String, nullable=False)
    last_name: str = db.Column(db.String, nullable=False)
    email: str = db.Column(db.String, unique=True, nullable=False)

    def __init__(
        self,
        username: str,
        password: str,
        role_id: int,
        first_name: str,
        last_name: str,
        email: str,
    ) -> None:
        self.username = username
        self.password = password
        self.role_id = role_id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email

    @classmethod
    def create(
        cls,
        username: str,
        password: str,
        role_id: int,
        first_name: str,
        last_name: str,
        email: str,
    ) -> "User":
        user = cls(
            username=username,
            password=password,
            role_id=role_id,
            first_name=first_name,
            last_name=last_name,
            email=email,
        )
        db.session.add(user)
        db.session.commit()
        return user
