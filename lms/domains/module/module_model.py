from dataclasses import dataclass

from sqlalchemy import ForeignKey, Text
from sqlalchemy.orm import relationship

from lms.adapters import BaseMixin, db


@dataclass
class Module(BaseMixin, db.Model):
    __tablename__ = "modules"

    title: str = db.Column(db.String(255), nullable=False)
    description: str = db.Column(Text, nullable=True)
    teacher_id: int = db.Column(db.Integer, ForeignKey("users.id"), nullable=True)
    teacher = relationship("User", backref="modules")

    def __init__(self, title: str, description: str, teacher_id: int) -> None:
        self.title = title
        self.description = description
        self.teacher_id = teacher_id

    @classmethod
    def create(cls, title: str, description: str, teacher_id: int) -> "Module":
        module = cls(title=title, description=description, teacher_id=teacher_id)
        db.session.add(module)
        db.session.commit()
        return module
