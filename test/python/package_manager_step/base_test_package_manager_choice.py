from abc import ABC
from typing import Any

from test.base_test_any_step import BaseTestAnyStep
from ytreza_builder.action_plan import ActionPlan
from ytreza_builder.python.python_project_builder import PythonPackageManagerChoice


class BaseTestPackageManagerChoice(BaseTestAnyStep, ABC):
    def from_step(self, action_plan: ActionPlan, configuration: dict[str, Any]):
        return PythonPackageManagerChoice(action_plan=action_plan, configuration=configuration)
