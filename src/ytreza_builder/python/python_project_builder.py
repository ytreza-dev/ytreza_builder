from typing import Any

from ytreza_builder.action_plan import ActionPlan
from ytreza_builder.command_handler_port import CommandHandlerPort
from ytreza_builder.python.deploy_choice.streamlit_on_scalingo import StreamlitWithScalingo
from ytreza_builder.python.package_manager.pipenv import PipenvBuiltIn
from ytreza_builder.python.package_manager.poetry import PoetryBuiltIn
from ytreza_builder.python.package_test_manager.pytest import PytestBuiltIn
from ytreza_builder.python.sample_choice.with_failing_test import WithFailingTest
from ytreza_builder.python.sample_choice.with_git_ignore import WithGitIgnore
from ytreza_builder.python.sample_choice.with_mypy import WithMypy
from ytreza_builder.python.sample_choice.with_streamlit import WithStreamLit


# @dataclass(frozen=True)
# class Configuration:
#     values: dict[str, Any]


class IsExecutable:
    def __init__(self, action_plan: ActionPlan, configuration: dict[str, Any]):
        self._configuration = configuration
        self._action_plan = action_plan

    def execute(self, command_handler: CommandHandlerPort):
        command_handler.execute_all(self._configuration, self._action_plan)


class PythonTestManagerChoice(IsExecutable, PytestBuiltIn):
    def then_add_samples(self):
        return PythonSampleChoice(self._action_plan, self._configuration)


class PythonDeployChoice(IsExecutable, StreamlitWithScalingo):
    pass


class PythonSampleChoice(IsExecutable, WithFailingTest, WithGitIgnore, WithMypy, WithStreamLit):
    def then_deploy(self) -> PythonDeployChoice:
        return PythonDeployChoice(self._action_plan, self._configuration)



class PythonPackageManagerChoice(IsExecutable, PoetryBuiltIn, PipenvBuiltIn):
    def __init__(self, action_plan: ActionPlan, configuration: dict[str, Any]):
        IsExecutable.__init__(self, action_plan, configuration)
        PoetryBuiltIn.__init__(self, action_plan)
        PipenvBuiltIn.__init__(self, action_plan)
        self._action_plan = action_plan
        self._configuration = configuration

    def then_test_project(self) -> PythonTestManagerChoice:
        return PythonTestManagerChoice(action_plan=self._action_plan, configuration=self._configuration)


class PythonBuiltin:
    def __init__(self, action_plan: ActionPlan, configuration: dict[str, Any]):
        self._action_plan = action_plan
        self._configuration = configuration
        

    def using_python(self) -> PythonPackageManagerChoice:
        return PythonPackageManagerChoice(action_plan=self._action_plan, configuration=self._configuration)


