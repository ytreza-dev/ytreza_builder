from typing import Any

import ytreza_builder.command as cmd
from test.base_test_any_step import BaseTestAnyStep
from ytreza_builder.action_plan import ActionPlan
from ytreza_builder.python.python_project_builder import PythonSampleChoice


class TestStreamlit(BaseTestAnyStep):
    def from_step(self, action_plan: ActionPlan, configuration: dict[str, Any]) -> PythonSampleChoice:
        return PythonSampleChoice(action_plan=action_plan, configuration=configuration)

    def action(self, step: PythonSampleChoice) -> PythonSampleChoice:
        return step.with_streamlit()

    def expected_command(self) -> list[cmd.Command]:
        return [
            cmd.InstallPackage(package_name="streamlit"),
            cmd.CopySample(source="python/streamlit", destination=cmd.ProjectPath()),
            cmd.CopySample(source="documentation/streamlit", destination=cmd.ProjectPath())
        ]
