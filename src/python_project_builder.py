from abc import ABC, abstractmethod
from typing import Any, Self

from src.command import CreateDirectory, ExecuteShell, Command
from src.command_handler_port import CommandHandlerPort
from src.package_manager.poetry import PoetryBuiltIn
from src.package_manager.pipenv import PipenvBuiltIn


class SystemFilePort(ABC):
    @abstractmethod
    def create_directory(self, path: str) -> None:
        pass

    @abstractmethod
    def execute(self, command_line: str, working_directory: str) -> None:
        pass


class PythonPackageManagerChoice(PoetryBuiltIn, PipenvBuiltIn):
    def __init__(self, system_file: SystemFilePort, commands: list[Command], configuration: dict[str, Any]):
        PoetryBuiltIn.__init__(self, commands)
        PipenvBuiltIn.__init__(self, commands)
        self._configuration: dict[str, Any] = configuration
        self._system_file = system_file

    def build(self) -> None:
        self._system_file.create_directory(self._full_project_folder())
        self._system_file.execute(command_line="python -m pip install --user poetry", working_directory=self._full_project_folder())

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

    def having_configuration(self, **kwargs) -> PythonPackageManagerChoice:
        return PythonPackageManagerChoice(system_file=self._system_file, commands=self._commands, configuration=kwargs)


class PythonProject:
    def __init__(self, system_file: SystemFilePort):
        self._commands: list[Command] = []
        self._configuration: dict[str, Any] = {}
        self._system_file = system_file

    def having_configuration(self, **kwargs) -> PythonPackageManagerChoice:
        return PythonPackageManagerChoice(system_file=self._system_file, commands=self._commands, configuration=kwargs)

    def execute(self, command_handler):
        pass

    def _full_project_folder(self):
        project_name = self._configuration["project_name"]
        project_folder = self._configuration["project_folder"]
        full_project_folder = f"{project_folder}/{project_name}"
        return full_project_folder
