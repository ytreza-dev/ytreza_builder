from typing import Any

from test.base_test_any_step import BaseTestAnyStep
import ytreza_builder.command as cmd
from ytreza_builder.action_plan import ActionPlan
from ytreza_builder.python_project_builder import PythonTestManagerChoice, PythonSampleChoice


class TestMypySample(BaseTestAnyStep):
    def from_step(self, action_plan: ActionPlan, configuration: dict[str, Any]):
        return PythonSampleChoice(action_plan=action_plan, configuration=configuration)

    def action(self, step: PythonSampleChoice):
        return step.with_mypy()

    def expected_command(self):
        return [cmd.CopySample(source="python/mypy", destination=cmd.ProjectPath())]
