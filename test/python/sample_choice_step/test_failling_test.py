from typing import Any

from test.base_test_any_step import BaseTestAnyStep
import ytreza_builder.command as cmd
from ytreza_builder.action_plan import ActionPlan
from ytreza_builder.python.python_project_builder import PythonTestManagerChoice, PythonSampleChoice


class TestFailingTestSample(BaseTestAnyStep):
    def from_step(self, action_plan: ActionPlan, configuration: dict[str, Any]):
        return PythonSampleChoice(action_plan=action_plan, configuration=configuration)

    def action(self, step: PythonSampleChoice):
        return step.with_failing_test()

    def expected_command(self):
        return [cmd.CopySample(source="python/failing_test", destination=cmd.ProjectPath())]
