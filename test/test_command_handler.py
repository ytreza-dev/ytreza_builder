import tempfile
from pathlib import Path

from src import command
from src.command import CreateDirectory
from src.command_handler import CommandHandler



def test_create_directory():
    with tempfile.TemporaryDirectory() as temp_dir:
        handler = CommandHandler()
        handler.execute_all(commands=[command.CreateDirectory(path=temp_dir + "/toto")])
        path = Path(temp_dir) / "toto"
        assert path.is_dir()

