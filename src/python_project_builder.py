from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any

from src.command import Command, CreateDirectory, ProjectPath
from src.command_handler_port import CommandHandlerPort
from src.package_manager.pipenv import PipenvBuiltIn
from src.package_manager.poetry import PoetryBuiltIn

# @dataclass(frozen=True)
# class Configuration:
#     values: dict[str, Any]


class IsExecutable:
    def __init__(self, commands: list[Command], configuration: dict[str, Any]):
        self._configuration = configuration
        self._commands = commands

    def _full_project_folder(self):
        project_name = self._configuration["project_name"]
        project_folder = self._configuration["project_folder"]
        full_project_folder = f"{project_folder}/{project_name}"
        return full_project_folder

    def execute(self, command_handler: CommandHandlerPort):
        self._commands.append(CreateDirectory(path=ProjectPath()))
        command_handler.execute_all(self._commands, {})


class SystemFilePort(ABC):
    @abstractmethod
    def create_directory(self, path: str) -> None:
        pass

    @abstractmethod
    def execute(self, command_line: str, working_directory: str) -> None:
        pass


class PythonTestManagerChoice:
    pass


class PythonPackageManagerChoice(IsExecutable, PoetryBuiltIn, PipenvBuiltIn):
    def __init__(self, commands: list[Command], configuration: dict[str, Any]):
        PoetryBuiltIn.__init__(self, commands)
        PipenvBuiltIn.__init__(self, commands)
        self._configuration: dict[str, Any] = configuration

    def _full_project_folder(self):
        project_name = self._configuration["project_name"]
        project_folder = self._configuration["project_folder"]
        full_project_folder = f"{project_folder}/{project_name}"
        return full_project_folder

    def then(self) -> PythonTestManagerChoice:
        return PythonTestManagerChoice()


class PythonProject:
    def __init__(self) -> None:
        self._commands: list[Command] = []

    def having_configuration(self, **kwargs) -> PythonPackageManagerChoice:
        return PythonPackageManagerChoice(commands=self._commands, configuration=kwargs)

