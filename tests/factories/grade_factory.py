import factory

from lms.domains import Grade

from .assignment_factory import AssignmentFactory
from .base import BaseFactory
from .user_factory import StudentFactory


class GradeFactory(BaseFactory):
    class Meta:
        model = Grade
        exclude = ["student", "assignment"]

    score = factory.Faker("pyfloat", positive=True, max_value=100)
    student = factory.SubFactory(StudentFactory)
    student_id = factory.SelfAttribute("student.id")
    assignment = factory.SubFactory(AssignmentFactory)
    assignment_id = factory.SelfAttribute("assignment.id")
