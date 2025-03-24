from dataclasses import dataclass


@dataclass(frozen=True)
class Poetry:
    pass


@dataclass(frozen=True)
class Pipenv:
    pass


PythonPackageManager = Poetry | Pipenv
