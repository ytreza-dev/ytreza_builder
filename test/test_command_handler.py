import tempfile
from pathlib import Path
from unittest.mock import patch

from src import command
from src.action_plan import ActionPlan
from src.command import ProjectPath
from src.command_handler import CommandHandler


def test_create_directory():
    with tempfile.TemporaryDirectory() as temp_dir:
        handler = CommandHandler()
        configuration = {"project_name": "toto", "project_folder": temp_dir}
        handler.execute_all(configuration=configuration,
                            action_plan=ActionPlan(commands=[command.CreateDirectory(path=ProjectPath())]))
        path = Path(temp_dir) / "toto"
        assert path.is_dir()

def test_execute():
    with patch("subprocess.run") as mock:
        handler = CommandHandler()
        handler.execute_all(configuration={}, action_plan=ActionPlan(
            commands=[command.ExecuteShell(command_line="echo 'hello'", working_directory="directory")]))
        mock.assert_called_once_with(["echo", "'hello'"], cwd="directory")
