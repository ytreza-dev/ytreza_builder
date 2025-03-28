from abc import ABC, abstractmethod
from typing import Any

from ytreza_builder.action_plan import ActionPlan


class CommandHandlerPort(ABC):
    @abstractmethod
    def execute_all(self, configuration: dict[str, Any], action_plan: ActionPlan):
        pass
