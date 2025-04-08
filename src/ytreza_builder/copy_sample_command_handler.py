from abc import ABC, abstractmethod
from dataclasses import dataclass
from string import Template

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

    @abstractmethod
    def read_file(self, path: str) -> str:
        pass


class FileCopierPort(ABC):
    @abstractmethod
    def copy(self, src: str, dst: str) -> None:
        pass

    @abstractmethod
    def write(self, dst: str, content: str):
        pass


class ConfigurationReaderPort(ABC):
    @abstractmethod
    def get(self, key) -> str:
        pass

    @abstractmethod
    def to_dict(self) -> dict[str, str]:
        pass


class SampleCopier:
    def __init__(self, file_reader: FileReaderPort, file_copier: FileCopierPort,
                 configuration_reader: ConfigurationReaderPort):
        self._file_reader = file_reader
        self._file_copier = file_copier
        self._configuration_reader = configuration_reader

    def execute(self, src: str, dst: str):
        self._copy_directory(src, dst)

    def _copy_directory(self, src: str, dst: str):
        src_directory = self._file_reader.read(src)

        for filename in src_directory.filenames:
            self._copy_file(src, filename, dst)

        for directory in src_directory.directories:
            self._copy_directory(src=f"{src}/{directory}", dst=(self._choose_directory(dst, directory)))

    def _copy_file(self, src: str, filename: str, dst: str):
        dst_file = self._choose_destination(dst, filename)
        if filename.endswith(".template"):
            self._file_copier.write(dst=dst_file,
                                    content=self._template_to_content(src, filename))
        else:
            self._file_copier.copy(src=f"{src}/{filename}", dst=dst_file)

    def _template_to_content(self, src: str, filename: str):
        return Template(self._file_reader.read_file(f"{src}/{filename}")).substitute(self._configuration_reader.to_dict())

    def _choose_directory(self, dst: str, directory: str) -> str:
        if directory.startswith("((") and directory.endswith("))"):
            return f"{dst}/{self._configuration_reader.get(directory[2:-2])}"
        return f"{dst}/{directory}"

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
        if filename_parts[-1] in ("sample", "template"):
            return ".".join(filename_parts[0: -2]) + "_sample" + "." + filename_parts[-2]
        return filename

    @staticmethod
    def _name_without_sample(filename: str) -> str:
        filename_parts = filename.split(".")
        if len(filename_parts) == 1:
            return filename
        if filename_parts[-1] in ("sample", "template"):
            if len(filename_parts) == 2:
                return filename_parts[0]
            return ".".join(filename_parts[0: -2]) + "." + filename_parts[-2]

        return filename
