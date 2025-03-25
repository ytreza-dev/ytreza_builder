from src.command_handler import CommandHandler
from src.python_project_builder import PythonProject


def main():
    python_project = PythonProject()
    command_handler = CommandHandler()
    (python_project
     .having_configuration(project_name="todolist_hexagon", project_folder="C:/Projets/python/todolist")
     .with_poetry().then_test_project()
     .with_pytest().then().use_failling_test_sample()
     .execute(command_handler=command_handler))


if __name__ == "__main__":
    main()