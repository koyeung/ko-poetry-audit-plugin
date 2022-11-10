from __future__ import annotations

from typing import TYPE_CHECKING, Iterable

from cleo.io.io import IO
from poetry.core.packages.dependency_group import MAIN_GROUP

if TYPE_CHECKING:
    from pathlib import Path

    from poetry.poetry import Poetry


class Auditor:
    """Class to check known vulnerabilities."""

    def __init__(self, poetry: Poetry, io: IO) -> None:
        self._poetry = poetry
        self._io = io
        self._groups: Iterable[str] = [MAIN_GROUP]

    def only_groups(self, groups: Iterable[str]) -> Auditor:
        self._groups = groups

        return self

    def audit(self, cwd: Path, output: IO | str) -> None:

        locked_repo = self._poetry.locker.locked_repository()

        package_versions = [
            f"{locked_package.name} - {locked_package.version} - {locked_package.category}"
            for locked_package in locked_repo.packages
            if locked_package.category in self._groups
        ]

        # to ignore locked_package.source_type is not None

        content = ", ".join(package_versions)
        content += "\n"

        if isinstance(output, IO):
            output.write(content)
        else:
            with (cwd / output).open("w", encoding="utf-8") as txt:
                txt.write(content)
