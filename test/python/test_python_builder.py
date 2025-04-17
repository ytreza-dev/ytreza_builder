import pytest

from test.system_file_for_test import SystemFileForTest
from ytreza_builder.python.python_project_builder import PythonPackageManagerChoice, \
    PythonTestManagerChoice, \
    PythonSampleChoice, PythonDeployChoice
from ytreza_builder.project_builder import LanguageChoice, Project


@pytest.fixture
def project(system_file: SystemFileForTest) -> Project:
    return Project()



def test_choose_package_manager_after_configuration(project: Project) -> None:
    assert isinstance(project.having_configuration(), LanguageChoice)


def test_choose_language_after_configuration(project: Project) -> None:
    assert isinstance(project.having_configuration().using_python(), PythonPackageManagerChoice)


def test_choose_test_manager_after_package_manager(project: Project) -> None:
    assert isinstance(project
                      .having_configuration().using_python()
                      .then_test_project()
                      , PythonTestManagerChoice)

def test_sample_choice_after_test_manager(project: Project) -> None:
    assert isinstance(project
                      .having_configuration().using_python()
                      .then_test_project().then_add_samples()
                      , PythonSampleChoice)


def test_deploy_choice_after_sample_choice(project: Project) -> None:
    assert isinstance(project
                      .having_configuration().using_python()
                      .then_test_project().then_add_samples().then_deploy()
                      , PythonDeployChoice)


