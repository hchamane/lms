import pytest

from lms.domains import Module
from tests.factories import ModuleFactory


@pytest.mark.usefixtures("wipe_modules_table")
class TestModuleModel:
    def test_module_init(self) -> None:
        module = ModuleFactory.build()
        assert isinstance(module, Module)
        assert isinstance(module.title, str)
        assert isinstance(module.description, (str, type(None)))
        assert isinstance(module.teacher_id, (int, type(None)))

    def test_module_init_with_missing_value(self) -> None:
        with pytest.raises(TypeError) as error:
            Module()

        assert str(error.value) == (
            "__init__() missing 3 required positional arguments: 'title', 'description', and 'teacher_id'"
        )

    def test_module_create(self) -> None:
        module = ModuleFactory.build()
        created_module = Module.create(title=module.title, description=module.description, teacher_id=module.teacher_id)

        assert isinstance(created_module, Module)
        assert created_module.title == module.title
        assert created_module.description == module.description
        assert created_module.teacher_id == module.teacher_id
