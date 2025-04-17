from dataclasses import dataclass, field
from typing import Any

from ytreza_builder.system_file_port import SystemFilePort


@dataclass(frozen=True)
class History:
    action: str
    param: dict[Any, Any] = field(default_factory=dict)

    def __eq__(self, other):
        return self.action == other.action and self.param == other.param


class SystemFileForTest(SystemFilePort):
    def __init__(self) -> None:
        self._history = []

    def history(self) -> list[History]:
        return self._history

    def create_directory(self, path: str) -> None:
        self._history.append(History(action="create_directory", param={"path": path}))

    def execute(self, command_line: str, working_directory: str) -> None:
        self._history.append(
            History(action="execute", param={"command_line": command_line, "working_directory": working_directory}))
