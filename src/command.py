from dataclasses import dataclass

from src.python_package_manager import PythonPackageManager


@dataclass(frozen=True)
class ProjectPath:
    pass


@dataclass(frozen=True, order=True)
class DummyCommand:
    value: str


@dataclass(frozen=True)
class CreateDirectory:
    path: ProjectPath


@dataclass(frozen=True)
class ExecuteShell:
    command_line: str
    working_directory: str


@dataclass(frozen=True)
class InstallPackage:
    package_name: str

PackageManager = PythonPackageManager

@dataclass()
class UsePackageManager:
    package_manager: PackageManager


@dataclass(frozen=True)
class CreateProject:
    pass


Command = DummyCommand | CreateDirectory | ExecuteShell | InstallPackage | UsePackageManager | CreateProject
