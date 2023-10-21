import pytest

from lms.domains import ModuleService
from tests.factories import ModuleFactory, UserFactory


@pytest.mark.usefixtures("wipe_modules_table")
class TestModuleService:
    def test_create_module(self, teacher_user) -> None:
        module = ModuleFactory.build()

        params = {
            "title": module.title,
            "description": module.description,
        }

        message, status = ModuleService().create(current_user=teacher_user, params=params)

        assert message == f"Module with title {module.title} successfully created"
        assert status == 201

    def test_create_module_with_missing_params(self, teacher_user) -> None:
        module = ModuleFactory.build()

        params = {
            "description": module.description,
        }

        message, status = ModuleService().create(current_user=teacher_user, params=params)

        assert message == "Something doesn't look right, please double check the parameters and try again"
        assert status == 422

    def test_create_module_with_missing_description(self, teacher_user) -> None:
        module = ModuleFactory.build()

        params = {
            "title": module.title,
        }

        message, status = ModuleService().create(current_user=teacher_user, params=params)

        assert message == "Something doesn't look right, please double check the parameters and try again"
        assert status == 422

    def test_create_module_without_teacher(self) -> None:
        module = ModuleFactory.build()

        params = {
            "title": module.title,
            "description": module.description,
        }

        message, status = ModuleService().create(current_user=None, params=params)

        assert message == "Something doesn't look right, please double check the parameters and try again"
        assert status == 422
