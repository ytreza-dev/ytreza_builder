import pytest

from conftest import SystemFileForTest, History, system_file, python_project, CommandHandlerForTest
from src.python_project_builder import PythonProject, CreateDirectory, ExecuteShell


def test_when_do_nothing(python_project: PythonProject, system_file: SystemFileForTest):
    assert system_file.history() == []
    command_handler = CommandHandlerForTest()
    python_project.execute(command_handler)
    assert command_handler.history() == []


@pytest.mark.parametrize("project_folder,project_name,expected", [
    ["c:/folder-1", "project_1", History(action="create_directory", param={"path": "c:/folder-1/project_1"})],
    ["c:/folder-1", "project-2", History(action="create_directory", param={"path": "c:/folder-1/project-2"})],
    ["c:/folder-2", "project-3", History(action="create_directory", param={"path": "c:/folder-2/project-3"})],
])
def test_create_project_directory_old(project_folder: str, project_name: str, expected: list[History],
                                      python_project: PythonProject, system_file: SystemFileForTest):
    (python_project
         .with_pipenv()
         .having_configuration(project_folder=project_folder, project_name=project_name)
         .build())
    assert expected in system_file.history()


@pytest.mark.parametrize("project_folder,project_name,expected", [
    ["c:/folder-1", "project_1", CreateDirectory(path="c:/folder-1/project_1")],
    ["c:/folder-1", "project-2", CreateDirectory(path="c:/folder-1/project-2")],
    ["c:/folder-2", "project-3", CreateDirectory(path="c:/folder-2/project-3")],
])
def test_create_project_directory(project_folder: str, project_name: str, expected: list[History],
                                  python_project: PythonProject, command_handler: CommandHandlerForTest):
    (python_project
     .with_pipenv()
     .having_configuration(project_folder=project_folder, project_name=project_name)
     .execute(command_handler))

    assert expected in command_handler.history()


def test_create_project_with_pipenv_old(python_project: PythonProject, system_file: SystemFileForTest):
    (python_project
         .with_pipenv()
         .having_configuration(project_name="test", project_folder="some directory")
         .build())


    assert History(action="execute",
                   param={
                       "command_line": "python -m pip install --user pipenv",
                       "working_directory": "some directory/test"
                   }) in system_file.history()


def test_create_project_with_pipenv(python_project: PythonProject, command_handler: CommandHandlerForTest):
    (python_project
     .with_pipenv()
     .having_configuration(project_name="test", project_folder="some directory")
     .execute(command_handler))

    assert ExecuteShell(command_line ="python -m pip install --user pipenv") in command_handler.history()
