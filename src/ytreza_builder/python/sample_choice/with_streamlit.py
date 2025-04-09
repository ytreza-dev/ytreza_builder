from typing import Self

from ytreza_builder import command
from ytreza_builder.action_plan import ActionPlan


class WithStreamLit:
    def __init__(self, action_plan: ActionPlan):
        self._action_plan = action_plan

    def with_streamlit(self) -> Self:
        self._action_plan = self._action_plan.prepare(
            command.InstallPackage(package_name="streamlit"),
            command.CopySample(source="python/streamlit", destination=command.ProjectPath()),
            command.CopySample(source="documentation/streamlit", destination=command.ProjectPath()))
        return self
