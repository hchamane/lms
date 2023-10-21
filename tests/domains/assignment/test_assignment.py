import json

import pytest

from tests.factories import AssignmentFactory, ModuleFactory


@pytest.mark.usefixtures("wipe_assignments_table")
class TestAssignment:
    def test_create_assignment(self, client, teacher_user) -> None:
        assignment = AssignmentFactory.build()
        module = ModuleFactory.create()

        params = {
            "title": assignment.title,
            "description": assignment.description,
            "module_id": module.id,
            "due_date": assignment.due_date,
        }

        response = client.post("/assignments/create", json=params)
        data = json.loads(response.data)

        assert response.status_code == 201
        assert data.get("message") == f"Assignment with title {assignment.title} successfully created"

    def test_create_assignment_with_missing_argument(self, client, teacher_user) -> None:
        assignment = AssignmentFactory.build()
        module = ModuleFactory.create()

        params = {
            "description": assignment.description,
            "module_id": module.id,
            "due_date": assignment.due_date,
        }

        response = client.post("/assignments/create", json=params)
        data = json.loads(response.data)

        assert response.status_code == 422
        assert data.get("message") == "Something doesn't look right, please double check the parameters and try again"

    def test_create_assignment_as_a_student(self, client, student_user) -> None:
        assignment = AssignmentFactory.build()
        module = ModuleFactory.create()

        params = {
            "title": assignment.title,
            "description": assignment.description,
            "module_id": module.id,
            "due_date": assignment.due_date,
        }

        response = client.post("/assignments/create", json=params)
        data = json.loads(response.data)

        assert response.status_code == 401
        assert data.get("message") == (
            "It appears you are not authorised to perform this action. "
            "Please double-check your authorization and try again."
        )
