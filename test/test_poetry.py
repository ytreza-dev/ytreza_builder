import pytest
from src.command import ExecuteShell
from src.package_manager.poetry import PoetryBuiltIn
from test.conftest import CommandHandlerForTest


def test_with_poetry():
    poetry = PoetryBuiltIn([])
    poetry_with_install = poetry.with_poetry()

    assert len(poetry_with_install._commands) == 1
    assert isinstance(poetry_with_install._commands[0], ExecuteShell)
    assert poetry_with_install._commands[0].command_line == "python -m pip install --user poetry"


def test_execute_poetry(command_handler: CommandHandlerForTest):
    poetry = PoetryBuiltIn([ExecuteShell(command_line="test command", working_directory=".")])
    poetry.with_poetry()
    poetry.execute(command_handler)

    history = command_handler.history()
    assert len(history) == 2
    assert history[0].command_line == "python -m pip install --user poetry"
    assert history[1].command_line == "test command"
