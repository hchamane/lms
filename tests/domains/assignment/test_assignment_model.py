from datetime import date

import pytest

from lms.domains import Assignment
from tests.factories import AssignmentFactory, ModuleFactory


@pytest.mark.usefixtures("wipe_assignments_table")
class TestAssignmentModel:
    def test_assignment_init(self) -> None:
        assignment = AssignmentFactory.build()
        assert isinstance(assignment, Assignment)
        assert isinstance(assignment.title, str)
        assert isinstance(assignment.description, (str, type(None)))
        assert isinstance(assignment.module_id, (int, type(None)))
        assert isinstance(assignment.due_date, (date, type(None)))

    def test_assignment_init_with_missing_value(self) -> None:
        with pytest.raises(TypeError) as error:
            Assignment()

        assert str(error.value) == (
            "__init__() missing 4 required positional arguments: 'title', 'description', 'module_id', and 'due_date'"
        )

    def test_assignment_create(self) -> None:
        module = ModuleFactory.create()
        assignment = AssignmentFactory.build(module_id=module.id)
        created_assignment = Assignment.create(
            title=assignment.title,
            description=assignment.description,
            module_id=assignment.module_id,
            due_date=assignment.due_date,
        )

        assert isinstance(created_assignment, Assignment)
        assert created_assignment.title == assignment.title
        assert created_assignment.description == assignment.description
