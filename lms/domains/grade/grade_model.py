from dataclasses import dataclass

from sqlalchemy import Float, ForeignKey
from sqlalchemy.orm import relationship

from lms.adapters import BaseMixin, db


@dataclass
class Grade(BaseMixin, db.Model):
    __tablename__ = "grades"

    student_id: int = db.Column(db.Integer, ForeignKey("users.id"), nullable=True)
    assignment_id: int = db.Column(db.Integer, ForeignKey("assignments.id"), nullable=True)
    score: float = db.Column(Float, nullable=False)

    student = relationship("User")
    assignment = relationship("Assignment", backref="grades")

    def __init__(self, score: float, student_id: int, assignment_id: int) -> None:
        self.score = score
        self.student_id = student_id
        self.assignment_id = assignment_id

    @classmethod
    def create(cls, score: float, student_id: int, assignment_id: int) -> "Grade":
        grade = cls(score=score, student_id=student_id, assignment_id=assignment_id)
        db.session.add(grade)
        db.session.commit()
        return grade
