from dataclasses import dataclass

from ytreza_builder.python.package_manager.type import PythonPackageManager


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

@dataclass()
class CopySample:
    source: str
    destination: AbstractPath


Command = DummyCommand | CreateDirectory | ExecuteShell | InstallPackage | UsePackageManager | CopySample