from src.command_handler import CommandHandler
from src.python_project_builder import PythonProject
from src.system_file_os import SystemFileOs


def main():
    python_project = PythonProject(SystemFileOs())
    command_handler = CommandHandler()
    python_project.with_pipenv().having_configuration(project_name="test", project_folder="c:/temp").execute(command_handler=command_handler)


if __name__ == "__main__":
    main()