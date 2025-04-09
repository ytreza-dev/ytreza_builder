from ytreza_builder import command
from ytreza_builder.action_plan import ActionPlan


class WithGitIgnore:
    def __init__(self, action_plan: ActionPlan):
        self._action_plan = action_plan

    def with_git_ignore(self):
        self._action_plan=self._action_plan.prepare(command.CopySample(source="python/gitignore", destination=command.ProjectPath()))
        return self

