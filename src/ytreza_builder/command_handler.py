import os
import shutil
import subprocess
from abc import ABC, abstractmethod
from pathlib import Path
from typing import assert_never, Any, Dict

import ytreza_builder.command as cmd
import ytreza_builder.python_package_manager as pm
from ytreza_builder import SAMPLE_DIR
from ytreza_builder.action_plan import ActionPlan
from ytreza_builder.command import ProjectPath
from ytreza_builder.copy_sample_command_handler import SampleCopier, FileReaderPort, Directory, FileCopierPort, \
    ConfigurationReaderPort
from ytreza_builder.command_handler_port import CommandHandlerPort


class PackageManagerStrategy(ABC):
    @abstractmethod
    def install(self, package_name: str, project_path: str) -> None:
        pass


class NoPackageManager(PackageManagerStrategy):
    def install(self, package_name: str, project_path: str) -> None:
        raise NotImplementedError("No package manager selected")


class PipenvPackageManager(PackageManagerStrategy):
    def install(self, package_name: str, project_path: str) -> None:
        subprocess.run(f"pipenv install {package_name}".split(" "), cwd=project_path)


class PoetryPackageManager(PackageManagerStrategy):
    def install(self, package_name: str, project_path: str) -> None:
        subprocess.run(f"poetry add {package_name}".split(" "), cwd=project_path)


class FileReader(FileReaderPort):
    def is_file(self, path: str) -> bool:
        return Path(path).is_file()

    def read(self, src: str) -> Directory:
        (root_path, directories, filenames) = next(os.walk(src))
        return Directory(path=root_path, directories=directories, filenames=filenames)



class FileCopier(FileCopierPort):
    def copy(self, src: str, dst: str) -> None:
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copy(src, dst)


class ConfigurationReader(ConfigurationReaderPort):
    def __init__(self, configuration: Dict[str, Any]):
        self._configuration = configuration

    def get(self, key) -> str:
        return self._configuration[key]


class CommandHandler(CommandHandlerPort):
    def __init__(self) -> None:
        self._package_manager_strategy: PackageManagerStrategy = NoPackageManager()

    def execute_all(self, configuration: dict[str, Any], action_plan: ActionPlan):
        for command in action_plan.commands:
            self._execute(command, configuration)

    def _execute(self, command: cmd.Command, configuration: dict[str, Any]) -> None:
        print(command)
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
                self._package_manager_strategy.install(package_name,
                                                       project_path=self._get_path(cmd.ProjectPath(), configuration))

            case cmd.CopySample(source=source, destination=destination):
                self._copy_sample(src=f"{SAMPLE_DIR}/{source}", dst=self._get_path(destination, configuration), configuration=configuration)

            case _:
                assert_never(command)

    @staticmethod
    def _copy_sample(src: str, dst: str, configuration: Dict[str, Any]) -> None:
        sample_copier = SampleCopier(file_reader=FileReader(), file_copier=FileCopier(), configuration_reader=ConfigurationReader(configuration))
        sample_copier.execute(src=src, dst=dst)

    def rename_files_from_directory(self, directory: str) -> None:
        for root, directories, files in os.walk(directory):
            for file in files:
                print(f"file: {file}")
                os.rename(os.path.join(root, file), os.path.join(root, file) + ".toto")
            for directory in directories:
                self.rename_files_from_directory(os.path.join(root, directory))
            print(os.listdir(root))

    def _create_directory(self, command: cmd.CreateDirectory, configuration: dict[str, Any]) -> None:
        project_path = self._get_path(command.path, configuration)
        Path(project_path).mkdir()

    def _execute_shell(self, command: cmd.ExecuteShell, configuration: dict[str, Any]):
        command_line = command.command_line.format(**configuration)
        subprocess.run(command_line.split(" "), cwd=self._get_path(command.working_directory, configuration))

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

    @staticmethod
    def _get_path(path: cmd.AbstractPath, configuration: dict[str, Any]) -> str:
        match path:
            case ProjectPath():
                project_name = configuration["project_name"]
                project_folder = configuration["project_folder"]
                return f"{project_folder}/{project_name}"

            case cmd.ProjectParentPath():
                project_folder = configuration["project_folder"]
                return project_folder

            case _:
                assert_never(path)
