from abc import ABC, abstractmethod
from typing import Any

from src.action_plan import ActionPlan
from src.command_handler_port import CommandHandlerPort
from src.package_manager.pipenv import PipenvBuiltIn
from src.package_manager.poetry import PoetryBuiltIn
from src.package_test_manager.pytest import PytestBuiltIn
from src.sample_choice.with_failing_test import WithFailingTest
from src.sample_choice.with_git_ignore import WithGitIgnore


# @dataclass(frozen=True)
# class Configuration:
#     values: dict[str, Any]


class IsExecutable:
    def __init__(self, action_plan: ActionPlan, configuration: dict[str, Any]):
        self._configuration = configuration
        self._action_plan = action_plan

    def execute(self, command_handler: CommandHandlerPort):
        command_handler.execute_all(self._configuration, self._action_plan)


class SystemFilePort(ABC):
    @abstractmethod
    def create_directory(self, path: str) -> None:
        pass

    @abstractmethod
    def execute(self, command_line: str, working_directory: str) -> None:
        pass


class PythonTestManagerChoice(IsExecutable, PytestBuiltIn):
    def then_add_samples(self):
        return PythonSampleChoice(self._action_plan, self._configuration)


class PythonSampleChoice(IsExecutable, WithFailingTest, WithGitIgnore):
    pass


class PythonPackageManagerChoice(IsExecutable, PoetryBuiltIn, PipenvBuiltIn):
    def __init__(self, action_plan: ActionPlan, configuration: dict[str, Any]):
        IsExecutable.__init__(self, action_plan, configuration)
        PoetryBuiltIn.__init__(self, action_plan)
        PipenvBuiltIn.__init__(self, action_plan)
        self._action_plan = action_plan
        self._configuration = configuration

    def then_test_project(self) -> PythonTestManagerChoice:
        return PythonTestManagerChoice(action_plan=self._action_plan, configuration=self._configuration)


class PythonProject:
    def __init__(self) -> None:
        self._action_plan = ActionPlan()


    def having_configuration(self, **kwargs) -> PythonPackageManagerChoice:
        return PythonPackageManagerChoice(action_plan=self._action_plan, configuration=kwargs)

