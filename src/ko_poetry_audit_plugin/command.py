from __future__ import annotations

from pathlib import Path

from cleo.helpers import option
from poetry.console.commands.group_command import GroupCommand
from poetry.core.packages.dependency_group import MAIN_GROUP

from .auditor import Auditor


class AuditCommand(GroupCommand):
    """Audit Command."""

    name = "audit"
    description = "Check known vulnerabilities."

    options = [
        option("output", "o", "The name of the output file.", flag=False),
        *GroupCommand._group_dependency_options(),
    ]

    @property
    def default_groups(self) -> set[str]:
        return {MAIN_GROUP}

    def handle(self) -> int:

        output = self.option("output")

        auditor = Auditor(self.poetry, self.io)
        auditor.only_groups(list(self.activated_groups))

        result = auditor.audit(Path.cwd(), output or self.io)
        return 0 if result else 1
