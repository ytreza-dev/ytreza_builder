from dataclasses import dataclass

from src.python_package_manager import PythonPackageManager


@dataclass(frozen=True)
class ProjectPath:
    pass


@dataclass()
class ProjectParentPath:
    pass


AbstractPath = ProjectPath | ProjectParentPath


@dataclass(frozen=True, order=True)
class DummyCommand:
    value: str


@dataclass(frozen=True)
class CreateDirectory:
    path: AbstractPath


@dataclass(frozen=True)
class ExecuteShell:
    command_line: str
    working_directory: AbstractPath

@dataclass(frozen=True)
class InstallPackage:
    package_name: str

PackageManager = PythonPackageManager


@dataclass()
class UsePackageManager:
    package_manager: PackageManager


Command = DummyCommand | CreateDirectory | ExecuteShell | InstallPackage | UsePackageManager