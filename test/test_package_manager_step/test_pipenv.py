import ytreza_builder.command as cmd
import ytreza_builder.python_package_manager as package_manager
from ytreza_builder.python_project_builder import PythonPackageManagerChoice
from test.test_package_manager_step.base_test_package_manager_choice import BaseTestPackageManagerChoice


class TestProjectWithPipenv(BaseTestPackageManagerChoice):
    def action(self, step : PythonPackageManagerChoice):
        return step.with_pipenv()

    def expected_command(self):
        return [
            cmd.CreateDirectory(cmd.ProjectPath()),
            cmd.ExecuteShell(command_line="python -m pip install --user pipenv", working_directory=cmd.ProjectPath()),
            cmd.UsePackageManager(package_manager.Pipenv()),
        ]
