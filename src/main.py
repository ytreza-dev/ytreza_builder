from src.python_project_builder import PythonProjectBuilder
from src.system_file_os import SystemFileOs


def main():
    python_project = PythonProjectBuilder(SystemFileOs())
    python_project.having_configuration(project_name="test", project_folder="c:/temp").build()


if __name__ == "__main__":
    main()