from ytreza_builder.command_handler  import CommandHandler
from ytreza_builder.python_project_builder import PythonProject


def main():
    python_project = PythonProject()
    command_handler = CommandHandler()
    (python_project
     .having_configuration(project_name="test_project", project_folder="C:/temp")
     .with_poetry().then_test_project()
     .with_pytest().then_add_samples().with_failing_test().with_git_ignore().with_mypy()
     .execute(command_handler=command_handler))

    python_project.having_configuration().with_poetry().then_test_project().with_pytest().then_add_samples().with_failing_test().with_git_ignore()

if __name__ == "__main__":
    main()