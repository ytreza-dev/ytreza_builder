import ytreza_builder.command as cmd
import ytreza_builder.python.package_manager.type
from test.python.package_manager_step.base_test_package_manager_choice import BaseTestPackageManagerChoice
from ytreza_builder.python.python_project_builder import PythonPackageManagerChoice


class TestProjectWithPipenv(BaseTestPackageManagerChoice):
    def action(self, step : PythonPackageManagerChoice) -> PythonPackageManagerChoice:
        return step.with_pipenv()

    def expected_command(self) -> list[cmd.Command]:
        return [
            cmd.CreateDirectory(cmd.ProjectPath()),
            cmd.ExecuteShell(command_line="python -m pip install --user pipenv", working_directory=cmd.ProjectPath()),
            cmd.UsePackageManager(ytreza_builder.python.package_manager.type.Pipenv()),
        ]
