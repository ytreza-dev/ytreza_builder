from abc import ABC, abstractmethod
from typing import Any

from src.command import Command


class CommandHandlerPort(ABC):
    @abstractmethod
    def execute_all(self, commands: list[Command], configuration: dict[str, Any]):
        pass
