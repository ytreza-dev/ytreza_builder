from abc import ABC

from test.base_test_any_step import BaseTestAnyStep
from src.action_plan import ActionPlan
from src.python_project_builder import PythonPackageManagerChoice


class BaseTestPackageManagerChoice(BaseTestAnyStep, ABC):
    def from_step(self, action_plan: ActionPlan):
        return PythonPackageManagerChoice(action_plan=action_plan, configuration={})
