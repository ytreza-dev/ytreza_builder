import pytest

from conftest import SystemFileForTest, History, system_file, python_project, CommandHandlerForTest
from src.command import CreateDirectory, ExecuteShell
from src.python_project_builder import PythonProject


def test_when_do_nothing(python_project: PythonProject, system_file: SystemFileForTest):
    assert system_file.history() == []
    command_handler = CommandHandlerForTest()
    python_project.execute(command_handler)
    assert command_handler.history() == []


@pytest.mark.parametrize("project_folder,project_name,expected", [
    ["c:/folder-1", "project_1", CreateDirectory(path="c:/folder-1/project_1")],
    ["c:/folder-1", "project-2", CreateDirectory(path="c:/folder-1/project-2")],
    ["c:/folder-2", "project-3", CreateDirectory(path="c:/folder-2/project-3")],
])
def test_create_project_directory(project_folder: str, project_name: str, expected: list[History],
                                  python_project: PythonProject, command_handler: CommandHandlerForTest):
    (python_project
     .having_configuration(project_folder=project_folder, project_name=project_name)
     .with_pipenv()
     .execute(command_handler))

    assert expected in command_handler.history()
