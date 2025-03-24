from dataclasses import dataclass
from typing import Self

from src.command import Command


@dataclass(frozen=True)
class ActionPlan:
    commands: tuple[Command, ...] = ()

    def prepare(self, command: Command) -> 'ActionPlan':
        return ActionPlan(commands=self.commands + (command,))


