from abc import ABC, abstractmethod

from src.command import Command


class CommandHandlerPort(ABC):
    @abstractmethod
    def execute_all(self, commands: list[Command]):
        pass
