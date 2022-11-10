from typing import NamedTuple


class Package(NamedTuple):
    """Package Identifier."""

    name: str
    version: str


class PoetryPackage(NamedTuple):
    """Package information from lock file."""

    name: str
    version: str
    category: str


class PypiPackage(NamedTuple):
    """Package with metadata from pypi."""

    name: str
    version: str
    metadata: dict | None


class VulnerablePackage(NamedTuple):
    """Package with metadata on vulnerabilities."""

    name: str
    version: str

    # it could be multiple vulnerabilities for each package/version
    vulnerabilities: list


class Vulnerability(NamedTuple):
    """Vulnerability."""

    package_name: str
    package_version: str

    # dependency group from poetry lock file
    dependency_group: str

    # fields from vulnerabilities dict
    id: str
    details: str
    link: str
    fixed_in: str
    withdrawn: str | None
