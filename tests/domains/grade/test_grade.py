import json

import pytest

from tests.factories import AssignmentFactory, GradeFactory, StudentFactory


@pytest.mark.usefixtures("wipe_grades_table")
class TestGrade:
    def test_create_grade(self, client, teacher_user) -> None:
        grade = GradeFactory.build()
        student = StudentFactory.create()
        assignment = AssignmentFactory.create()

        params = {"student_id": student.id, "assignment_id": assignment.id, "score": grade.score}

        response = client.post("/grades/create", json=params)
        data = json.loads(response.data)

        assert response.status_code == 201
        assert (
            data.get("message") == f"Grade for student {student.id} and assignment {assignment.id} successfully created"
        )

    def test_create_grade_with_missing_argument(self, client, teacher_user) -> None:
        grade = GradeFactory.build()

        params = {"assignment_id": grade.assignment_id, "score": grade.score}

        response = client.post("/grades/create", json=params)
        data = json.loads(response.data)

        assert response.status_code == 422
        assert data.get("message") == "Something doesn't look right, please double check the parameters and try again"

    def test_create_grade_as_a_student(self, client, student_user) -> None:
        grade = GradeFactory.build()
        student = StudentFactory.create()
        assignment = AssignmentFactory.create()

        params = {"student_id": student.id, "assignment_id": assignment.id, "score": grade.score}

        response = client.post("/grades/create", json=params)
        data = json.loads(response.data)

        assert response.status_code == 401
        assert data.get("message") == (
            "It appears you are not authorised to perform this action. "
            "Please double-check your authorization and try again."
        )

    def test_view_grades_as_student(self, client, student_user) -> None:
        assignment = AssignmentFactory.create()
        another_assignment = AssignmentFactory.create()
        grade_one = GradeFactory.create(student_id=student_user.id, assignment_id=assignment.id, score=30)
        grade_two = GradeFactory.create(student_id=student_user.id, assignment_id=another_assignment.id, score=50)

        response = client.get("/grades/view")
        data = json.loads(response.data)

        assert grade_one.assignment.id in [grade["assignment_id"] for grade in data]
        assert grade_two.assignment.id in [grade["assignment_id"] for grade in data]
        assert response.status_code == 200

    def test_view_grades_as_non_student(self, client, teacher_user) -> None:
        response = client.get("/grades/view")
        data = json.loads(response.data)

        assert data.get("message") == "You are not a student, so there is no grades to see"
        assert response.status_code == 422
