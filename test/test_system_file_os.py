import tempfile
from pathlib import Path
from unittest.mock import patch

from src.system_file_os import SystemFileOs


def test_create_directory():
    with tempfile.TemporaryDirectory() as temp_dir:
        system = SystemFileOs()
        system.create_directory(temp_dir + "/toto")
        path = Path(temp_dir) / "toto"
        assert path.is_dir()


def test_execute():
    with patch("subprocess.run") as mock:
        system = SystemFileOs()
        system.execute("echo 'hello'", "directory")
        mock.assert_called_once_with(["echo", "'hello'"], cwd="directory")

