from __future__ import annotations

from typing import TYPE_CHECKING

from poetry.plugins.application_plugin import ApplicationPlugin

from .command import AuditCommand

if TYPE_CHECKING:
    from poetry.console.application import Application
    from poetry.console.commands.command import Command


class AuditApplicationPlugin(ApplicationPlugin):
    """Audit application plugin."""

    @property
    def commands(self) -> list[type[Command]]:
        return [AuditCommand]

    def activate(self, application: Application) -> None:
        super().activate(application=application)
