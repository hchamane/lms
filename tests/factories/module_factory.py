import factory

from lms.domains import Module

from .base import BaseFactory
from .user_factory import TeacherFactory


class ModuleFactory(BaseFactory):
    class Meta:
        model = Module
        exclude = ["teacher"]

    title = factory.Faker("sentence", nb_words=4)
    description = factory.Faker("paragraph")
    teacher = factory.SubFactory(TeacherFactory)
    teacher_id = factory.SelfAttribute("teacher.id")
