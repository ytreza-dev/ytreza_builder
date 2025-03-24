import subprocess
from pathlib import Path
from typing import assert_never, Any

import src.command as cmd
from src.action_plan import ActionPlan
from src.command import ProjectPath
from src.command_handler_port import CommandHandlerPort


class CommandHandler(CommandHandlerPort):
    def execute_all(self, configuration: dict[str, Any], action_plan: ActionPlan):
        for command in action_plan.commands:
            self._execute(command, configuration)

    def _execute(self, command: cmd.Command, configuration: dict[str, Any]) -> None:
        match command:
            case cmd.CreateDirectory():
                self._create_directory(command, configuration)

            case cmd.ExecuteShell(command_line=command_line, working_directory=working_directory):
                self._execute_shell(command_line=command_line, working_directory=working_directory)

            case cmd.DummyCommand(value=value):
                raise NotImplementedError(f"DummyCommand {value} is not implemented")

            case cmd.InstallPackage(package_name=package_name):
                self._install_package(package_name=package_name)

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

    @staticmethod
    def _execute_shell(command_line: str, working_directory: str):
        subprocess.run(command_line.split(" "), cwd=working_directory)

    @staticmethod
    def _install_package(package_name: str):
        subprocess.run(f"poetry add {package_name}".split(" "), cwd=None)

