import factory

from lms.domains import Assignment

from .base import BaseFactory
from .module_factory import ModuleFactory


class AssignmentFactory(BaseFactory):
    class Meta:
        model = Assignment
        exclude = ["module"]

    title = factory.Faker("sentence", nb_words=4)
    description = factory.Faker("paragraph")
    module = factory.SubFactory(ModuleFactory)
    module_id = factory.SelfAttribute("module.id")
    due_date = factory.Faker("future_date")
