import pytest

from conftest import SystemFileForTest, History, system_file, python_project
from python_project_builder import PythonProjectBuilder


def test_when_do_nothing(system_file: SystemFileForTest):
    assert system_file.history() == []


@pytest.mark.parametrize("project_folder,project_name,expected", [
    ["c:/folder-1", "project_1", [History(action="create_directory", param={"path": "c:/folder-1/project_1"})]],
    ["c:/folder-1", "project-2", [History(action="create_directory", param={"path": "c:/folder-1/project-2"})]],
    ["c:/folder-2", "project-3", [History(action="create_directory", param={"path": "c:/folder-2/project-3"})]],
])
def test_create_project_directory(project_folder: str, project_name: str, expected: list[History],
                                  python_project: PythonProjectBuilder, system_file: SystemFileForTest):
    (python_project
     .having_configuration(project_folder=project_folder, project_name=project_name)
     .build())
    assert system_file.history() == expected
