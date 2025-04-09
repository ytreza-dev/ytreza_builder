from ytreza_builder.command_handler  import CommandHandler
from ytreza_builder.project_builder import Project


def main():
    python_project = Project()
    command_handler = CommandHandler()
    (python_project
     .having_configuration(project_name="test_project", project_folder="C:/temp")
     .using_python()
     .with_poetry().then_test_project()
     .with_pytest().then_add_samples().with_streamlit().with_git_ignore().with_mypy().then_deploy().streamlit_on_scalingo()
     .execute(command_handler=command_handler))

if __name__ == "__main__":
    main()