from src.python_project_builder import PythonProject, PythonPackageManagerChoice, PythonTestManagerChoice
from test.conftest import python_project


def test_choose_package_manager_after_configuration(python_project: PythonProject):
    assert isinstance(python_project.having_configuration(), PythonPackageManagerChoice)


def test_choose_test_manager_after_package_manager(python_project: PythonProject):
    assert isinstance(python_project
                      .having_configuration()
                      .then()
                      , PythonTestManagerChoice)
