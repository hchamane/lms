from dataclasses import dataclass
from datetime import date

from sqlalchemy import Date, ForeignKey, Text
from sqlalchemy.orm import relationship

from lms.adapters import BaseMixin, db


@dataclass
class Assignment(BaseMixin, db.Model):
    __tablename__ = "assignments"

    title: str = db.Column(db.String(255), nullable=False)
    description: str = db.Column(Text, nullable=True)
    module_id: int = db.Column(db.Integer, ForeignKey("modules.id"), nullable=True)
    due_date: date = db.Column(Date, nullable=True)

    module = relationship("Module", backref="assignments")

    def __init__(self, title: str, description: str, module_id: int, due_date: date) -> None:
        self.title = title
        self.description = description
        self.module_id = module_id
        self.due_date = due_date

    @classmethod
    def create(cls, title: str, description: str, module_id: int, due_date: date) -> "Assignment":
        assignment = cls(title=title, description=description, module_id=module_id, due_date=due_date)
        db.session.add(assignment)
        db.session.commit()
        return assignment
