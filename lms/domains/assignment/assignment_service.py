from .assignment_model import Assignment


class AssignmentService:
    def create(self, current_user, params: dict[str, str | int | float]) -> tuple[str, int]:
        title = params.get("title")
        description = params.get("description")
        module_id = params.get("module_id")
        due_date = params.get("due_date")

        if not all([title, description, module_id, due_date]):
            return "Something doesn't look right, please double check the parameters and try again", 422

        Assignment.create(title=title, description=description, module_id=module_id, due_date=due_date)

        return f"Assignment with title {title} successfully created", 201
