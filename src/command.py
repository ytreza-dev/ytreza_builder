from dataclasses import dataclass


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


Command = DummyCommand | CreateDirectory | ExecuteShell | InstallPackage

