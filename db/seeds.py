import secrets

from typing import TYPE_CHECKING

from lms.app import app
from tests.factories import AssignmentFactory, GradeFactory, ModuleFactory, StudentFactory, TeacherFactory, UserFactory

if TYPE_CHECKING:
    from lms.domains import Assignment, User


def create_admin_user() -> "User":
    admin_user = "admin"
    admin_password = "$2b$12$6I5Ls.Z7UNfYZZHV.ElhJ.qu/.g/2CW3W9VzQPpP.7YdgxYman.2S"
    admin = UserFactory.create(
        username=admin_user,
        first_name=admin_user,
        last_name=admin_user,
        password=admin_password,
        email="admin@admin.com",
        auth_token=secrets.token_hex(24),
    )

    return admin


def create_teacher_user() -> "User":
    teacher_user = "teacher"
    teacher_password = "$2b$12$hHg0grc8eHimaZmoB42IReoAio8sA/GdymEVcgha/EIrucPKkGk/S"

    teacher = TeacherFactory.create(
        username=teacher_user,
        first_name=teacher_user,
        last_name=teacher_user,
        password=teacher_password,
        email="teacher@teacher.com",
        auth_token=secrets.token_hex(24),
    )

    return teacher


def create_student_user() -> "User":
    student_user = "student"
    student_password = "$2b$12$Lin26rHVfL8anWmBFwovdO54CiyAr6Let8ZD/m0PbQNHO24ScG6EK"

    student = StudentFactory.create(
        username=student_user,
        first_name=student_user,
        last_name=student_user,
        password=student_password,
        email="student@student.com",
        auth_token=secrets.token_hex(24),
    )

    return student


def create_assignment(teacher_id: int, student_id: int) -> "Assignment":
    module = ModuleFactory.create(teacher_id=teacher_id)
    assignment = AssignmentFactory.create(module_id=module.id)
    return assignment


def create_grade(assignment_id: int, student_id: int) -> None:
    GradeFactory.create(assignment_id=assignment_id, student_id=student_id)


def seed_data() -> None:
    with app.app_context():
        create_admin_user()
        teacher = create_teacher_user()
        student = create_student_user()
        assignment = create_assignment(teacher_id=teacher.id, student_id=student.id)
        create_grade(assignment_id=assignment.id, student_id=student.id)
        GradeFactory.create()


if __name__ == "__main__":
    seed_data()
