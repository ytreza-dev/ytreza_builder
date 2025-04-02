from abc import ABC, abstractmethod
from dataclasses import dataclass

from ytreza_builder import command as cmd


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

    @abstractmethod
    def is_file(self, path: str) -> bool:
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
        self._copy_directory(src, dst)

    def _copy_directory(self, src: str, dst: str):
        directory = self._file_reader.read(src)

        for filename in directory.filenames:
            self._file_copier.copy(src=f"{src}/{filename}", dst=self._choose_destination(dst, filename))

        for directory in directory.directories:
            self._copy_directory(src=f"{src}/{directory}", dst=f"{dst}/{directory}")

    def _choose_destination(self, dst: str, filename: str) -> str:
        name_without_sample = f"{dst}/{self._name_without_sample(filename)}"

        if self._file_exist(name_without_sample):
            return  f"{dst}/{self.name_when_exist(filename)}"

        return name_without_sample

    def _file_exist(self, name_when_not_exist):
        return self._file_reader.is_file(name_when_not_exist)

    @staticmethod
    def name_when_exist(filename: str) -> str:
        filename_parts = filename.split(".")
        if filename_parts[-1] == "sample":
            return ".".join(filename_parts[0: -2]) + "_" + filename_parts[-1] + "." + filename_parts[-2]
        return filename

    @staticmethod
    def _name_without_sample(filename: str) -> str:
        filename_parts = filename.split(".")
        if filename_parts[-1] == "sample":
            return ".".join(filename_parts[0: -2]) + "." + filename_parts[-2]
        return filename

