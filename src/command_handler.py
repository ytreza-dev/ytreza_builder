from src.python_project_builder import CommandHandlerPort, Command


class CommandHandler(CommandHandlerPort):
    def execute_all(self, commands: list[Command]):
        pass
