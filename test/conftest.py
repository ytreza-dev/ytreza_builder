from dataclasses import dataclass, field
from typing import Any

import pytest

from src.python_project_builder import SystemFilePort, PythonProjectBuilder


class SystemFileForTest(SystemFilePort):
    def __init__(self):
        self._history = []

    def history(self) -> list[Any]:
        return self._history

    def create_directory(self, path: str):
        self._history.append(History(action="create_directory", param={"path": path}))


@dataclass
class History:
    action: str
    param: dict = field(default_factory=dict)


@pytest.fixture
def system_file() -> SystemFileForTest:
    return SystemFileForTest()


@pytest.fixture
def python_project(system_file: SystemFileForTest) -> PythonProjectBuilder:
    return PythonProjectBuilder(system_file=system_file)
