import subprocess
from abc import ABC, abstractmethod
from pathlib import Path
from typing import assert_never, Any

import src.command as cmd
import src.python_package_manager as pm
from src.action_plan import ActionPlan
from src.command import ProjectPath
from src.command_handler_port import CommandHandlerPort


class PackageManagerStrategy(ABC):
    @abstractmethod
    def install(self, package_name: str) -> None:
        pass


class NoPackageManager(PackageManagerStrategy):
    def install(self, package_name: str) -> None:
        raise NotImplementedError("No package manager selected")


class PipenvPackageManager(PackageManagerStrategy):
    def install(self, package_name: str) -> None:
        subprocess.run(f"pipenv install {package_name}".split(" "), cwd=None)


class PoetryPackageManager(PackageManagerStrategy):
    def install(self, package_name: str) -> None:
        subprocess.run(f"poetry add {package_name}".split(" "), cwd=None)


class CommandHandler(CommandHandlerPort):
    def __init__(self) -> None:
        self._package_manager_strategy: PackageManagerStrategy = NoPackageManager()

    def execute_all(self, configuration: dict[str, Any], action_plan: ActionPlan):
        for command in action_plan.commands:
            self._execute(command, configuration)

    def _execute(self, command: cmd.Command, configuration: dict[str, Any]) -> None:
        match command:
            case cmd.CreateDirectory():
                self._create_directory(command, configuration)

            case cmd.ExecuteShell():
                self._execute_shell(command, configuration)

            case cmd.DummyCommand(value=value):
                raise NotImplementedError(f"DummyCommand {value} is not implemented")

            case cmd.UsePackageManager(package_manager=package_manager):
                self._select_package_manager(package_manager)

            case cmd.InstallPackage(package_name=package_name):
                self._package_manager_strategy.install(package_name)

            case _:
                assert_never(command)

    def _create_directory(self, command: cmd.CreateDirectory, configuration: dict[str, Any]) -> None:
        match command.path:
            case ProjectPath():
                project_path = self._full_project_folder(configuration)
                Path(project_path).mkdir()

            case _:
                assert_never(command.path)

    @staticmethod
    def _full_project_folder(configuration: dict[str, Any]):
        project_name = configuration["project_name"]
        project_folder = configuration["project_folder"]
        full_project_folder = f"{project_folder}/{project_name}"
        return full_project_folder

    def _execute_shell(self, command: cmd.ExecuteShell, configuration: dict[str, Any]):
        subprocess.run(command.command_line.split(" "), cwd=self._full_project_folder(configuration))

    @staticmethod
    def _install_package(package_name: str):
        subprocess.run(f"poetry add {package_name}".split(" "), cwd=None)

    def _select_package_manager(self, package_manager: cmd.PackageManager):
        match package_manager:
            case pm.Poetry():
                self._package_manager_strategy = PoetryPackageManager()

            case pm.Pipenv():
                self._package_manager_strategy = PipenvPackageManager()

            case _:
                assert_never(package_manager)
