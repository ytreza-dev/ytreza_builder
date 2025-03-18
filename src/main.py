from src.python_project_builder import PythonProject
from src.system_file_os import SystemFileOs


def main():
    python_project = PythonProject(SystemFileOs())
    python_project.with_pipenv().having_configuration(project_name="test", project_folder="c:/temp").build()


if __name__ == "__main__":
    main()