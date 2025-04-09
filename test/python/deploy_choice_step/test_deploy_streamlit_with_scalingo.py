from typing import Any

import ytreza_builder.command as cmd
from test.base_test_any_step import BaseTestAnyStep
from ytreza_builder.action_plan import ActionPlan
from ytreza_builder.python.python_project_builder import PythonDeployChoice


class TestDeployStreamlitWithScalingo(BaseTestAnyStep):
    def from_step(self, action_plan: ActionPlan, configuration: dict[str, Any]):
        return PythonDeployChoice(action_plan=action_plan, configuration=configuration)

    def action(self, step: PythonDeployChoice):
        return step.streamlit_on_scalingo()

    def expected_command(self):
        return [cmd.CopySample(source="python/scalingo_streamlit", destination=cmd.ProjectPath())]
