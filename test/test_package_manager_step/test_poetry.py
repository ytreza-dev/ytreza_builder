import ytreza_builder.command as cmd
import ytreza_builder.python_package_manager as package_manager
from ytreza_builder.python_project_builder import PythonPackageManagerChoice
from test.test_package_manager_step.base_test_package_manager_choice import BaseTestPackageManagerChoice


class TestProjectWithPoetry(BaseTestPackageManagerChoice):
    def action(self, step: PythonPackageManagerChoice):
        return step.with_poetry()

    def expected_command(self):
        return [
            cmd.ExecuteShell(command_line="python -m pip install --user poetry", working_directory=cmd.ProjectParentPath()),
            cmd.ExecuteShell(command_line="poetry new {project_name}", working_directory=cmd.ProjectParentPath()),
            cmd.UsePackageManager(package_manager.Poetry()),
        ]
