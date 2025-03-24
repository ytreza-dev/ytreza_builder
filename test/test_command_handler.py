import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest

import src.python_package_manager as pm
import src.command as cmd
from src.action_plan import ActionPlan
from src.command import ProjectPath
from src.command_handler import CommandHandler


def test_create_directory():
    with tempfile.TemporaryDirectory() as temp_dir:
        handler = CommandHandler()
        configuration = {"project_name": "toto", "project_folder": temp_dir}
        handler.execute_all(configuration=configuration,
                            action_plan=ActionPlan(commands=(cmd.CreateDirectory(path=ProjectPath()),)))
        path = Path(temp_dir) / "toto"
        assert path.is_dir()

def test_execute_shell():
    with patch("subprocess.run") as mock:
        handler = CommandHandler()
        handler.execute_all(configuration={}, action_plan=ActionPlan(
            commands=(cmd.ExecuteShell(command_line="echo 'hello'", working_directory="directory"),)))
        mock.assert_called_once_with(["echo", "'hello'"], cwd="directory")

@pytest.mark.parametrize("package_manager, expected", [
    [pm.Poetry(), "poetry add pytest"],
    [pm.Pipenv(), "pipenv install pytest"],
])
def test_install_python_package(package_manager, expected: str):
    with patch("subprocess.run") as mock:
        handler = CommandHandler()
        handler.execute_all(configuration={}, action_plan=ActionPlan(
            commands=(
                cmd.UsePackageManager(package_manager),
                cmd.InstallPackage(package_name="pytest"),)))

        mock.assert_called_once_with(expected.split(" "), cwd=None)
