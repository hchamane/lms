import pytest

from lms.domains import GradeService
from tests.factories import AssignmentFactory, GradeFactory, StudentFactory


@pytest.mark.usefixtures("wipe_grades_table")
class TestGradeService:
    def test_create_grade(self) -> None:
        grade = GradeFactory.build()
        student = StudentFactory.create()
        assignment = AssignmentFactory.create()

        params = {"student_id": student.id, "assignment_id": assignment.id, "score": grade.score}

        message, status = GradeService().create(params=params)

        assert message == f"Grade for student {student.id} and assignment {assignment.id} successfully created"
        assert status == 201

    def test_create_grade_with_missing_params(self) -> None:
        grade = GradeFactory.build()

        params = {"assignment_id": grade.assignment_id, "score": grade.score}

        message, status = GradeService().create(params=params)

        assert message == "Something doesn't look right, please double check the parameters and try again"
        assert status == 422
