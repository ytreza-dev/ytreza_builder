# ytreza builder

This tool allow to create easily project with the state of the art of our team.

## How to use the tool ?

```python
from src.command_handler import CommandHandler
from src.python_project_builder import PythonProject


def main():
    python_project = PythonProject()
    command_handler = CommandHandler()
    (python_project
     .having_configuration(project_name="project name", project_folder="c:/temp")
     .with_poetry().then_test_project()
     .with_pytest()
     .execute(command_handler=command_handler))


if __name__ == "__main__":
    main()
```

## known environment
- windows

