from ytreza_builder.action_plan import ActionPlan
from ytreza_builder.python.python_project_builder import IsExecutable, PythonBuiltin


class LanguageChoice(IsExecutable, PythonBuiltin):
    pass


class Project:
    def __init__(self) -> None:
        self._action_plan = ActionPlan()

    def having_configuration(self, **kwargs) -> LanguageChoice:
        return LanguageChoice(action_plan=self._action_plan, configuration=kwargs)
