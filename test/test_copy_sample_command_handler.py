import os
from dataclasses import dataclass

import pytest

from src.copy_sample_command_handler import FileReaderPort, Directory, FileCopierPort, SampleCopier


class FileReaderForTest(FileReaderPort):
    def __init__(self) -> None:
        self._directories: dict[str, Directory] = {}

    def read(self, src: str) -> Directory:
        if src not in self._directories:
            raise FileNotFoundError(f"No directory {src}")

        return self._directories[src]

    def feed(self, directory: Directory):
        self._directories[directory.path] = directory


@dataclass
class Copy:
    src: str
    dst: str


class FileCopierForTest(FileCopierPort):
    def __init__(self):
        self._history = []

    def history(self) -> list[Copy]:
        return self._history

    def copy(self, src: str, dst: str) -> None:
        self._history.append(Copy(src=src, dst=dst))


@pytest.fixture
def file_copier():
    return FileCopierForTest()


@pytest.fixture
def file_reader():
    return FileReaderForTest()


@pytest.fixture
def sample_copier(file_reader: FileReaderForTest, file_copier: FileCopierForTest):
    return SampleCopier(file_copier=file_copier, file_reader=file_reader)


def test_when_nothing(file_copier: FileCopierForTest):
    assert file_copier.history() == []


def test_copy_one_file(sample_copier: SampleCopier, file_reader: FileReaderForTest, file_copier: FileCopierForTest):
    file_reader.feed(directory=Directory(path="src", directories=[], filenames=["file_1"]))
    sample_copier.execute(src="src", dst="dst")
    assert file_copier.history() == [Copy(src="src/file_1", dst="dst/file_1")]


def test_copy_another_file(sample_copier: SampleCopier, file_reader: FileReaderForTest, file_copier: FileCopierForTest):
    file_reader.feed(directory=Directory(path="src", directories=[], filenames=["file_2"]))
    sample_copier.execute(src="src", dst="dst")
    assert file_copier.history() == [Copy(src="src/file_2", dst="dst/file_2")]


def test_copy_many_files(sample_copier: SampleCopier, file_reader: FileReaderForTest, file_copier: FileCopierForTest):
    file_reader.feed(directory=Directory(path="src", directories=[], filenames=["file_1", "file_2"]))
    sample_copier.execute(src="src", dst="dst")
    assert file_copier.history() == [
        Copy(src="src/file_1", dst="dst/file_1"),
        Copy(src="src/file_2", dst="dst/file_2")]


def test_copy_directory(sample_copier: SampleCopier, file_reader: FileReaderForTest, file_copier: FileCopierForTest):
    file_reader.feed(directory=Directory(path="src", directories=["dir_1", "dir_2"], filenames=["file_1", "file_2"]))
    file_reader.feed(directory=Directory(path="src/dir_1", directories=[], filenames=["file_3"]))
    file_reader.feed(directory=Directory(path="src/dir_2", directories=["dir_3"], filenames=["file_4"]))
    file_reader.feed(directory=Directory(path="src/dir_2/dir_3", directories=[], filenames=["file_5"]))

    sample_copier.execute(src="src", dst="dst")
    assert file_copier.history() == [
        Copy(src="src/file_1", dst="dst/file_1"),
        Copy(src="src/file_2", dst="dst/file_2"),
        Copy(src="src/dir_1/file_3", dst="dst/dir_1/file_3"),
        Copy(src="src/dir_2/file_4", dst="dst/dir_2/file_4"),
        Copy(src="src/dir_2/dir_3/file_5", dst="dst/dir_2/dir_3/file_5"),
    ]


@pytest.mark.parametrize("filename, expected", [
    ["file_1.py.sample", Copy(src="src/file_1.py.sample", dst="dst/file_1_sample.py")],
    ["file_2.py.sample", Copy(src="src/file_2.py.sample", dst="dst/file_2_sample.py")],
    ["file.3.py.sample", Copy(src="src/file.3.py.sample", dst="dst/file.3_sample.py")],
    ["f.i.l.e.4.py.sample", Copy(src="src/f.i.l.e.4.py.sample", dst="dst/f.i.l.e.4_sample.py")],
])
def test_rename_sample(filename: str, expected: Copy, sample_copier: SampleCopier, file_reader: FileReaderForTest,
                       file_copier: FileCopierForTest):
    file_reader.feed(directory=Directory(path="src", directories=[], filenames=[filename]))
    sample_copier.execute(src="src", dst="dst")
    assert file_copier.history() == [expected]


