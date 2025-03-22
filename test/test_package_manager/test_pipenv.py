from conftest import CommandHandlerForTest
from src.command import ExecuteShell
from src.package_manager.pipenv import PipenvBuiltIn


def test_create_project_with_pipenv(command_handler: CommandHandlerForTest):
    project = PipenvBuiltIn(commands=[])
    (project
     .with_pipenv()
     .execute(command_handler))

    assert ExecuteShell(command_line="python -m pip install --user pipenv",
                        working_directory=".") in command_handler.history()
