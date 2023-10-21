import pytest

from lms.domains import AssignmentService
from tests.factories import AssignmentFactory, ModuleFactory


@pytest.mark.usefixtures("wipe_assignments_table")
class TestAssignmentService:
    def test_create_assignment(self, teacher_user) -> None:
        assignment = AssignmentFactory.build()
        module = ModuleFactory.create()

        params = {
            "title": assignment.title,
            "description": assignment.description,
            "module_id": module.id,
            "due_date": assignment.due_date,
        }

        message, status = AssignmentService().create(current_user=teacher_user, params=params)

        assert message == f"Assignment with title {assignment.title} successfully created"
        assert status == 201

    def test_create_assignment_with_missing_params(self, teacher_user) -> None:
        assignment = AssignmentFactory.build()
        module = ModuleFactory.create()

        params = {
            "description": assignment.description,
            "module_id": module.id,
        }

        message, status = AssignmentService().create(current_user=teacher_user, params=params)

        assert message == "Something doesn't look right, please double check the parameters and try again"
        assert status == 422

    def test_create_assignment_without_module(self, teacher_user) -> None:
        assignment = AssignmentFactory.build()

        params = {"title": assignment.title, "description": assignment.description}

        message, status = AssignmentService().create(current_user=teacher_user, params=params)

        assert message == "Something doesn't look right, please double check the parameters and try again"
        assert status == 422

    def test_create_assignment_without_due_date(self, teacher_user) -> None:
        assignment = AssignmentFactory.build()
        module = ModuleFactory.create()

        params = {
            "title": assignment.title,
            "description": assignment.description,
            "module_id": module.id,
        }

        message, status = AssignmentService().create(current_user=teacher_user, params=params)

        assert message == "Something doesn't look right, please double check the parameters and try again"
        assert status == 422
