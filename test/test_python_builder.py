import pytest

from conftest import History, python_project, CommandHandlerForTest
from src.command import CreateDirectory
from src.python_project_builder import PythonProject, PythonPackageManagerChoice, PythonTestManagerChoice


@pytest.mark.parametrize("project_folder,project_name,expected", [
    ["c:/folder-1", "project_1", CreateDirectory(path="c:/folder-1/project_1")],
    ["c:/folder-1", "project-2", CreateDirectory(path="c:/folder-1/project-2")],
    ["c:/folder-2", "project-3", CreateDirectory(path="c:/folder-2/project-3")],
])
def test_create_project_directory(project_folder: str, project_name: str, expected: list[History],
                                  python_project: PythonProject, command_handler: CommandHandlerForTest):
    (python_project
     .having_configuration(project_folder=project_folder, project_name=project_name)
     .execute(command_handler))

    assert expected in command_handler.history()


def test_choose_package_manager_after_configuration(python_project: PythonProject):
    assert isinstance(python_project.having_configuration(), PythonPackageManagerChoice)


def test_choose_test_manager_after_package_manager(python_project: PythonProject):
    assert isinstance(python_project
                      .having_configuration()
                      .then()
                      , PythonTestManagerChoice)
