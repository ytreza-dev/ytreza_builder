import src.command as cmd
import src.python_package_manager as package_manager
from src.python_project_builder import PythonPackageManagerChoice
from test.test_package_manager.base_test_package_manager_choice import BaseTestPackageManagerChoice


class TestProjectWithPoetry(BaseTestPackageManagerChoice):
    def action(self, step: PythonPackageManagerChoice):
        return step.with_poetry()

    def expected_command(self):
        return [
            cmd.ExecuteShell(command_line="python -m pip install --user poetry", working_directory="."),
            cmd.UsePackageManager(package_manager.Poetry()),
            cmd.CreateDirectory(cmd.ProjectPath()),
            cmd.ExecuteShell(command_line="poetry init", working_directory="."),
        ]
