import os

from functools import wraps
from typing import Any, Final

from lms.domains.user.user_model import User

HERE: Final[str] = os.path.dirname(os.path.realpath(__file__))


def authorize_teacher(function) -> Any:
    @wraps(function)
    def check_teacher_auth(*args, **kwargs) -> Any:
        access_token = None

        try:
            with open(f"{HERE}/../../.auth", "r") as file:
                access_token = file.read().strip()
        except FileNotFoundError:
            pass

        current_user = User.find_by(auth_token=access_token)

        if not current_user:
            return {
                "message": "It appears you provided an invalid token. "
                "Please double-check your authorization and try again."
            }, 401

        if not current_user.is_teacher():
            return {
                "message": "It appears you are not authorised to perform this action. "
                "Please double-check your authorization and try again."
            }, 401

        return function(*args, **kwargs, current_user=current_user)

    return check_teacher_auth


def authorize_student(function) -> Any:
    @wraps(function)
    def check_student_auth(*args, **kwargs) -> Any:
        access_token = None

        try:
            with open(f"{HERE}/../../.auth", "r") as file:
                access_token = file.read().strip()
        except FileNotFoundError:
            pass

        current_user = User.find_by(auth_token=access_token)

        if not current_user:
            return {
                "message": "It appears you provided an invalid token. "
                "Please double-check your authorization and try again."
            }, 401

        if not current_user.is_student():
            return {
                "message": "It appears you are not authorised to perform this action. "
                "Please double-check your authorization and try again."
            }, 401

        return function(*args, **kwargs, current_user=current_user)

    return check_student_auth


def authorize_student_or_teacher(function) -> Any:
    @wraps(function)
    def check_student_or_teacher_auth(*args, **kwargs) -> Any:
        access_token = None

        try:
            with open(f"{HERE}/../../.auth", "r") as file:
                access_token = file.read().strip()
        except FileNotFoundError:
            pass

        current_user = User.find_by(auth_token=access_token)

        if not current_user:
            return {
                "message": "It appears you provided an invalid token. "
                "Please double-check your authorization and try again."
            }, 401

        return function(*args, **kwargs, current_user=current_user)

    return check_student_or_teacher_auth
