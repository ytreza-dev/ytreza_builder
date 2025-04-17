import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest

import ytreza_builder.command as cmd
from ytreza_builder.action_plan import ActionPlan
from ytreza_builder.command import ProjectPath, ProjectParentPath
from ytreza_builder.command_handler import CommandHandler
from ytreza_builder.python.package_manager import type


def test_create_directory_from_project_path() -> None:
    with tempfile.TemporaryDirectory() as temp_dir:
        handler = CommandHandler()
        configuration = {"project_name": "toto", "project_folder": temp_dir}
        handler.execute_all(configuration=configuration,
                            action_plan=ActionPlan(commands=(cmd.CreateDirectory(path=ProjectPath()),)))
        path = Path(temp_dir) / "toto"
        assert path.is_dir()


def test_create_directory_from_project_parent_path() -> None:
    with tempfile.TemporaryDirectory() as temp_dir:
        handler = CommandHandler()
        configuration = {"project_name": "toto", "project_folder": temp_dir + "/folder"}
        handler.execute_all(configuration=configuration,
                            action_plan=ActionPlan(commands=(cmd.CreateDirectory(path=ProjectParentPath()),)))
        path = Path(temp_dir + "/folder")
        assert path.is_dir()


def test_execute_shell() -> None:
    with patch("subprocess.run") as mock:
        handler = CommandHandler()
        handler.execute_all(configuration={"project_name": "project", "project_folder": "directory"}, action_plan=ActionPlan(
            commands=(cmd.ExecuteShell(command_line="echo 'hello {project_name}'", working_directory=cmd.ProjectPath()),)))
        mock.assert_called_once_with(["echo", "'hello", "project'"], cwd="directory/project")

@pytest.mark.parametrize("package_manager, expected", [
    [type.Poetry(), "poetry add pytest"],
    [type.Pipenv(), "pipenv install pytest"],
])
def test_install_python_package(package_manager: type.PythonPackageManager, expected: str) -> None:
    with patch("subprocess.run") as mock:
        handler = CommandHandler()
        handler.execute_all(configuration={"project_name": "project", "project_folder": "directory"}, action_plan=ActionPlan(
            commands=(
                cmd.UsePackageManager(package_manager),
                cmd.InstallPackage(package_name="pytest"),)))

        mock.assert_called_once_with(expected.split(" "), cwd="directory/project")


def test_copy_sample() -> None:
    with tempfile.TemporaryDirectory() as temp_dir:
        handler = CommandHandler()
        handler.execute_all(configuration={"project_name": "project", "project_folder": temp_dir}, action_plan=ActionPlan(commands=(cmd.CopySample(source="python/streamlit", destination=ProjectPath()), )))
        assert (Path(temp_dir) / "project" / "src" / "project" / "main.py").is_file()


def test_write_template() -> None:
    with tempfile.TemporaryDirectory() as temp_dir:
        handler = CommandHandler()
        handler.execute_all(configuration={"project_name": "project", "project_folder": temp_dir}, action_plan=ActionPlan(commands=(cmd.CopySample(source="python/scalingo_streamlit", destination=ProjectPath()), )))
        assert (Path(temp_dir) / "project" / "Procfile").read_text() == "web: streamlit run ./src/project/main.py --server.port $PORT"

