from test.conftest import python_project
from ytreza_builder.python_project_builder import PythonProject, PythonPackageManagerChoice, PythonTestManagerChoice, \
    PythonSampleChoice, PythonDeployChoice


def test_choose_package_manager_after_configuration(python_project: PythonProject):
    assert isinstance(python_project.having_configuration(), PythonPackageManagerChoice)


def test_choose_test_manager_after_package_manager(python_project: PythonProject):
    assert isinstance(python_project
                      .having_configuration()
                      .then_test_project()
                      , PythonTestManagerChoice)

def test_sample_choice_after_test_manager(python_project: PythonProject):
    assert isinstance(python_project
                      .having_configuration()
                      .then_test_project().then_add_samples()
                      , PythonSampleChoice)


def test_deploy_choice_after_sample_choice(python_project: PythonProject):
    assert isinstance(python_project
                      .having_configuration()
                      .then_test_project().then_add_samples().then_deploy()
                      , PythonDeployChoice)


