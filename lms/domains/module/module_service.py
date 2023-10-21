import os

from typing import Final, Literal

from .module_model import Module

HERE: Final[str] = os.path.dirname(os.path.realpath(__file__))


class ModuleService:
    def create(self, current_user, params: dict[str, str | int]) -> tuple[str, Literal[422] | Literal[201]]:
        title = params.get("title")
        description = params.get("description")
        teacher_id = current_user.id

        if not all([title, description, teacher_id]):
            return "Something doesn't look right, please double check the parameters and try again", 422

        Module.create(title=title, description=description, teacher_id=teacher_id)

        return f"Module with title {title} successfully created", 201
