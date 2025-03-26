from abc import ABC, abstractmethod
from dataclasses import dataclass

from src import command as cmd


class CopySampleHandler:
    def handle(self, command: cmd.CopySample) -> None:
        pass


@dataclass
class Directory:
    path: str
    directories: list[str]
    filenames: list[str]


class FileReaderPort(ABC):
    @abstractmethod
    def read(self, src: str) -> Directory:
        pass


class FileCopierPort(ABC):
    @abstractmethod
    def copy(self, src: str, dst: str) -> None:
        pass


class SampleCopier:
    def __init__(self, file_reader: FileReaderPort, file_copier: FileCopierPort):
        self._file_reader = file_reader
        self._file_copier = file_copier

    def execute(self, src: str, dst: str):
        self._copy(dst, src)

    def _copy(self, dst, src):
        root_directory = self._file_reader.read(src)
        for filename in root_directory.filenames:
            self._file_copier.copy(src=f"{src}/{filename}", dst=f"{dst}/{self._rename_file(filename)}")
        for directory in root_directory.directories:
            self._copy(src=f"{src}/{directory}", dst=f"{dst}/{directory}")

    @staticmethod
    def _rename_file(filename: str) -> str:
        filename_parts = filename.split(".")
        if filename_parts[-1] == "sample":
            return ".".join(filename_parts[0: -2] + [filename_parts[-1], filename_parts[-2]])
        return filename
