import tempfile
from pathlib import Path

from system_file_os import SystemFileOs


def test_create_directory():
    with tempfile.TemporaryDirectory() as temp_dir:
        system = SystemFileOs()
        system.create_directory(temp_dir + "/toto")
        path = Path(temp_dir) / "toto"
        assert path.is_dir()
