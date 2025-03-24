import src.command as cmd
from src.python_project_builder import PythonPackageManagerChoice
from test.test_package_manager.base_test_package_manager_choice import BaseTestPackageManagerChoice


class TestProjectWithPipenv(BaseTestPackageManagerChoice):
    def action(self, step : PythonPackageManagerChoice):
        return step.with_pipenv()

    def expected_command(self):
        return [
            cmd.ExecuteShell(command_line="python -m pip install --user pipenv", working_directory="."),
            cmd.UsePackageManager(name="pipenv")
        ]
