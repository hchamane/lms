from .assignment import Assignment, AssignmentService, assignment_domain
from .feature_switch import FeatureSwitch
from .grade import Grade, GradeService, grade_domain
from .module import Module, ModuleService, module_domain
from .user import User, UserRole, UserService, user_domain

__all__ = [
    "assignment_domain",
    "Assignment",
    "AssignmentService",
    "FeatureSwitch",
    "Grade",
    "GradeService",
    "grade_domain",
    "User",
    "UserRole",
    "user_domain",
    "UserService",
    "Module",
    "ModuleService",
    "module_domain",
]
