from abc import ABC, abstractmethod
from typing import Self, Any


class SystemFilePort(ABC):
    @abstractmethod
    def create_directory(self, path: str) -> None:
        pass

    @abstractmethod
    def execute(self, command_line: str, working_directory: str) -> None:
        pass


class PythonProjectBuilder:
    def __init__(self, system_file: SystemFilePort, configuration: dict[str, Any]):
        self._configuration: dict[str, Any] = configuration
        self._system_file = system_file

    def build(self) -> None:
        self._system_file.create_directory(self._full_project_folder())
        self._system_file.execute(command_line="python -m pip install --user pipenv", working_directory=self._full_project_folder())

    def _full_project_folder(self):
        project_name = self._configuration["project_name"]
        project_folder = self._configuration["project_folder"]
        full_project_folder = f"{project_folder}/{project_name}"
        return full_project_folder


class PythonProjectConfiguration:
    def __init__(self, system_file: SystemFilePort):
        self._system_file = system_file

    def having_configuration(self, **kwargs) -> PythonProjectBuilder:
        return PythonProjectBuilder(self._system_file, configuration=kwargs)


class PythonProject:
    def __init__(self, system_file: SystemFilePort):
        self._configuration: dict[str, Any] = {}
        self._system_file = system_file

    def with_pipenv(self) -> PythonProjectConfiguration:
        return PythonProjectConfiguration(self._system_file)
