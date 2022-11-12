from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Container, Iterable

from cleo.io.io import IO
from poetry.core.packages.dependency_group import MAIN_GROUP

from .packages import Package, PoetryPackage
from .pypi_warehouse import get_vulnerable_packages
from .vulnerabilities import (
    format_vulnerabilities,
    get_vulnerabilities,
    is_all_withdrawn,
)

if TYPE_CHECKING:
    from pathlib import Path

    from poetry.poetry import Poetry
    from poetry.repositories import Repository

LOGGER = logging.getLogger(__name__)


class Auditor:
    """Class to check known vulnerabilities."""

    def __init__(self, poetry: Poetry, io: IO) -> None:
        self._poetry = poetry
        self._io = io
        self._groups: Iterable[str] = [MAIN_GROUP]

    def only_groups(self, groups: Iterable[str]) -> Auditor:
        self._groups = groups

        return self

    def audit(self, cwd: Path, output: IO | str) -> bool:
        """Perform audit.

        :return: `True` if no known vulnerabilities left.
        """
        locked_repo = self._poetry.locker.locked_repository()

        packages = get_locked_packages(
            locked_repo=locked_repo, groups=set(self._groups)
        )
        vulnerable_packages = get_vulnerable_packages(packages.keys())
        vulnerabilities = get_vulnerabilities(
            poetry_packages=packages, vulnerable_packages=vulnerable_packages
        )

        vulnerabilities_left = True

        if not vulnerabilities:
            content = "No known vulnerabilities found\n"
            vulnerabilities_left = False
        else:
            content = "Found vulnerabilities\n"
            content += format_vulnerabilities(vulnerabilities)
            content += "\n"

            if is_all_withdrawn(vulnerabilities):
                content += "All vulnerablilities withdrawn\n"
                vulnerabilities_left = False

        if isinstance(output, IO):
            output.write(content)
        else:
            with (cwd / output).open("w", encoding="utf-8") as txt:
                txt.write(content)

        return not vulnerabilities_left


def get_locked_packages(
    locked_repo: Repository, groups: Container[str]
) -> dict[Package, PoetryPackage]:
    """Get packages of dependency groups from lock file.

    Package with source type defined would be ignored.
    """
    LOGGER.info(f"get packages list from dependencies {groups=}")

    packages = {}
    for locked_package in locked_repo.packages:

        name = locked_package.name
        version = str(locked_package.version)
        group = locked_package.category

        if not group in groups:
            LOGGER.warning(f"packages {name=}, {version=} in {group=} skipped")
            continue

        name = locked_package.name
        version = str(locked_package.version)
        if locked_package.source_type is not None:
            LOGGER.warning(
                f"packages {name=}, {version=} of {locked_package.source_type=} skipped"
            )
            continue

        packages[Package(name=name, version=version)] = PoetryPackage(
            name=name, version=version, category=group
        )

    return packages
