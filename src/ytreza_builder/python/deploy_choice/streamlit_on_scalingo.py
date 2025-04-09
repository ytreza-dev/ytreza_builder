from ytreza_builder import command
from typing import Self

from ytreza_builder.action_plan import ActionPlan


class StreamlitWithScalingo:
    def __init__(self, action_plan: ActionPlan):
        self._action_plan = action_plan

    def streamlit_on_scalingo(self) -> Self:
        self._action_plan = self._action_plan.prepare(
            command.CopySample(source="python/scalingo_streamlit", destination=command.ProjectPath()))
        return self

