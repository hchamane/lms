from .grade_model import Grade


class GradeService:
    def create(self, params: dict[str, int | float]) -> tuple[str, int]:
        student_id = params.get("student_id")
        assignment_id = params.get("assignment_id")
        score = params.get("score")

        if not all([student_id, assignment_id, score]):
            return "Something doesn't look right, please double check the parameters and try again", 422

        Grade.create(student_id=student_id, assignment_id=assignment_id, score=score)

        return f"Grade for student {student_id} and assignment {assignment_id} successfully created", 201
