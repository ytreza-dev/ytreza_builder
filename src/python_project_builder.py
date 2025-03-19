from abc import ABC, abstractmethod
from typing import Any

from src.command import CreateDirectory, ExecuteShell, Command


class SystemFilePort(ABC):
    @abstractmethod
    def create_directory(self, path: str) -> None:
        pass

    @abstractmethod
    def execute(self, command_line: str, working_directory: str) -> None:
        pass


class CommandHandlerPort(ABC):
    @abstractmethod
    def execute_all(self, commands: list[Command]):
        pass


class PythonProjectBuilder:
    def __init__(self, system_file: SystemFilePort, commands: list[Command], configuration: dict[str, Any]):
        self._configuration: dict[str, Any] = configuration
        self._system_file = system_file
        self._commands = commands

    def build(self) -> None:
        self._system_file.create_directory(self._full_project_folder())
        self._system_file.execute(command_line="python -m pip install --user pipenv", working_directory=self._full_project_folder())

    def _full_project_folder(self):
        project_name = self._configuration["project_name"]
        project_folder = self._configuration["project_folder"]
        full_project_folder = f"{project_folder}/{project_name}"
        return full_project_folder

    def execute(self, command_handler: CommandHandlerPort):
        self._commands.append(CreateDirectory(path=self._full_project_folder()))
        command_handler.execute_all(self._commands)


class PythonProjectConfiguration:
    def __init__(self, system_file: SystemFilePort, commands: list[Command]):
        self._system_file = system_file
        self._commands = commands

    def having_configuration(self, **kwargs) -> PythonProjectBuilder:
        return PythonProjectBuilder(system_file=self._system_file, commands=self._commands, configuration=kwargs)




class PythonProject:
    def __init__(self, system_file: SystemFilePort):
        self._commands: list[Command] = []
        self._configuration: dict[str, Any] = {}
        self._system_file = system_file

    def with_pipenv(self) -> PythonProjectConfiguration:
        self._commands.append(ExecuteShell(command_line="python -m pip install --user pipenv"))
        return PythonProjectConfiguration(self._system_file, self._commands)

    def execute(self, command_handler):
        pass
