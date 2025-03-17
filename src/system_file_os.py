from pathlib import Path

from src.python_project_builder import SystemFilePort


class SystemFileOs(SystemFilePort):
    def create_directory(self, path: str) -> None:
        Path(path).mkdir()
