from src.command_handler import CommandHandler
from src.python_project_builder import PythonProject


def main():
    python_project = PythonProject()
    command_handler = CommandHandler()
    (python_project
     .having_configuration(project_name="test5", project_folder="c:/temp")
     .with_poetry().then()
     .with_pytest()
     .execute(command_handler=command_handler))


if __name__ == "__main__":
    main()