import os
import subprocess
from pathlib import Path

from src.python_project_builder import SystemFilePort


class SystemFileOs(SystemFilePort):
    def create_directory(self, path: str) -> None:
        Path(path).mkdir()

    def execute(self, command_line: str, working_directory: str) -> None:
        subprocess.run(command_line.split(" "), cwd=working_directory)


