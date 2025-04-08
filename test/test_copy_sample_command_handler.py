from dataclasses import dataclass
from typing import Dict

import pytest

from ytreza_builder.copy_sample_command_handler import FileReaderPort, Directory, FileCopierPort, SampleCopier, \
    ConfigurationReaderPort


class FileReaderForTest(FileReaderPort):
    def __init__(self) -> None:
        self._contents: dict[str, str] = {}
        self._directories: dict[str, Directory] = {}
        self._existing_files: list[str] = []

    def read(self, src: str) -> Directory:
        if src not in self._directories:
            raise FileNotFoundError(f"No directory {src}")

        return self._directories[src]

    def read_file(self, path: str) -> str:
        return self._contents[path]

    def is_file(self, path: str) -> bool:
        return path in self._existing_files

    def feed(self, directory: Directory):
        self._directories[directory.path] = directory

    def feed_content(self, path: str, content: str):
        self._contents[path] = content

    def feed_exist(self, path: str):
        self._existing_files.append(path)


@dataclass
class Copy:
    src: str
    dst: str


@dataclass
class Write:
    dst: str
    content: str

History = Copy | Write


class FileCopierForTest(FileCopierPort):
    def __init__(self):
        self._history = []

    def history(self) -> list[History]:
        return self._history

    def copy(self, src: str, dst: str) -> None:
        self._history.append(Copy(src=src, dst=dst))

    def write(self, dst: str, content: str):
        self._history.append(Write(dst=dst, content=content))


@pytest.fixture
def file_copier():
    return FileCopierForTest()


@pytest.fixture
def file_reader():
    return FileReaderForTest()


class ConfigurationReaderForTest(ConfigurationReaderPort):
    def __init__(self) -> None:
        self._configuration : Dict[str, str] = {}

    def get(self, key) -> str:
        return self._configuration[key]

    def feed(self, key: str, value: str):
        self._configuration[key] = value

    def feed_bis(self, **configuration):
        self._configuration = configuration

    def to_dict(self) -> dict[str, str]:
        return self._configuration



@pytest.fixture
def configuration_reader() -> ConfigurationReaderForTest:
    return ConfigurationReaderForTest()


@pytest.fixture
def sample_copier(file_reader: FileReaderForTest, file_copier: FileCopierForTest, configuration_reader: ConfigurationReaderForTest):
    return SampleCopier(file_copier=file_copier, file_reader=file_reader, configuration_reader=configuration_reader)


def test_when_nothing(file_copier: FileCopierForTest):
    assert file_copier.history() == []


@pytest.mark.parametrize("filename, expected", [
    ["file_1", Copy(src="src/file_1", dst="dst/file_1")],
    ["file_2", Copy(src="src/file_2", dst="dst/file_2")],
    ["sample", Copy(src="src/sample", dst="dst/sample")],
    ["template", Copy(src="src/template", dst="dst/template")],
    ["file.template.txt", Copy(src="src/file.template.txt", dst="dst/file.template.txt")],
])
def test_copy_one_file(filename: str, expected: History, sample_copier: SampleCopier, file_reader: FileReaderForTest, file_copier: FileCopierForTest):
    file_reader.feed(directory=Directory(path="src", directories=[], filenames=[filename]))
    sample_copier.execute(src="src", dst="dst")
    assert file_copier.history() == [expected]


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


@pytest.mark.parametrize("filename, existing, expected", [
    ["file_1.py.sample", "dst/file_1.py", Copy(src="src/file_1.py.sample", dst="dst/file_1_sample.py")],
    ["file_2.py.sample", "dst/file_2.py", Copy(src="src/file_2.py.sample", dst="dst/file_2_sample.py")],
    ["file.3.py.sample", "dst/file.3.py", Copy(src="src/file.3.py.sample", dst="dst/file.3_sample.py")],
    ["f.i.l.e.4.py.sample", "dst/f.i.l.e.4.py", Copy(src="src/f.i.l.e.4.py.sample", dst="dst/f.i.l.e.4_sample.py")],
])
def test_rename_sample_when_file_exist(filename: str, expected: Copy, existing: str, sample_copier: SampleCopier, file_reader: FileReaderForTest,
                       file_copier: FileCopierForTest):
    file_reader.feed(directory=Directory(path="src", directories=[], filenames=[filename]))
    file_reader.feed_exist(path=existing)
    sample_copier.execute(src="src", dst="dst")
    assert file_copier.history() == [expected]

@pytest.mark.parametrize("filename, expected", [
    ["file.py.sample", Copy(src="src/file.py.sample", dst="dst/file.py")],
    ["file.sample", Copy(src="src/file.sample", dst="dst/file")],
])
def test_remove_sample_extension_when_file_does_not_exist(filename:str, expected: History, sample_copier: SampleCopier, file_reader: FileReaderForTest, file_copier: FileCopierForTest):
    file_reader.feed(directory=Directory(path="src", directories=[], filenames=[filename]))
    sample_copier.execute(src="src", dst="dst")
    assert file_copier.history() == [expected]


@pytest.mark.parametrize("key, value, expected", [
    ["key", "value", Copy(src="src/((key))/file", dst="dst/value/file")],
    ["otherKey", "otherValue", Copy(src="src/((otherKey))/file", dst="dst/otherValue/file")],
])
def test_read_configuration_for_directories(key: str, value: str, expected: Copy, sample_copier: SampleCopier, file_reader: FileReaderForTest, file_copier: FileCopierForTest, configuration_reader: ConfigurationReaderForTest):
    file_reader.feed(directory=Directory(path="src", directories=[f"(({key}))"], filenames=[]))
    file_reader.feed(directory=Directory(path=f"src/(({key}))", directories=[], filenames=["file"]))
    configuration_reader.feed(key=key, value=value)
    sample_copier.execute(src="src", dst="dst")
    assert file_copier.history() == [expected]


@pytest.mark.parametrize("template, expected_content, configuration", [
    ["content without variable", "content without variable", {}],
    ["other content without variable", "other content without variable", {}],
    ["${project_name}", "myProject", {"project_name": "myProject"}],
    ["${project_name}", "other project", {"project_name": "other project"}],
])
def test_fill_template(template: str, expected_content: str, configuration: dict[str, str], sample_copier: SampleCopier, file_reader: FileReaderForTest, file_copier: FileCopierForTest, configuration_reader: ConfigurationReaderForTest):
    file_reader.feed(directory=Directory(path="src", directories=[], filenames=["file.py.template"]))
    file_reader.feed_content(path="src/file.py.template", content=template)
    configuration_reader.feed_bis(**configuration)
    sample_copier.execute(src="src", dst="dst")
    assert file_copier.history() == [Write(dst="dst/file.py", content=expected_content)]



@pytest.mark.parametrize("filename, existing, expected", [
    ["file_1.py.template", "dst/file_1.py", Write(dst="dst/file_1_sample.py", content="some content")],
    ["file_2.py.template", "dst/file_2.py", Write(dst="dst/file_2_sample.py", content="some content")],
    ["file.3.py.template", "dst/file.3.py", Write(dst="dst/file.3_sample.py", content="some content")],
    ["f.i.l.e.4.py.template", "dst/f.i.l.e.4.py", Write(dst="dst/f.i.l.e.4_sample.py", content="some content")],
])
def test_rename_template_when_file_exist(filename: str, expected: Copy, existing: str, sample_copier: SampleCopier, file_reader: FileReaderForTest,
                       file_copier: FileCopierForTest):
    file_reader.feed(directory=Directory(path="src", directories=[], filenames=[filename]))
    file_reader.feed_exist(path=existing)
    file_reader.feed_content(f"src/{filename}", "some content")
    sample_copier.execute(src="src", dst="dst")
    assert file_copier.history() == [expected]
