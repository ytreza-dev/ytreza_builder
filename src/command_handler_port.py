from abc import ABC, abstractmethod
from typing import Any

from src.action_plan import ActionPlan
from src.command import Command


class CommandHandlerPort(ABC):
    @abstractmethod
    def execute_all(self, configuration: dict[str, Any], action_plan: ActionPlan):
        pass
