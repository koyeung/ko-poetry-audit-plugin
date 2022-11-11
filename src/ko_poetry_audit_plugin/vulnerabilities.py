import logging
from typing import Collection, Iterable

from tabulate import tabulate

from .packages import Package, PoetryPackage, Vulnerability, VulnerablePackage

LOGGER = logging.getLogger(__name__)

#: map from display column name to `Vulnerability` field name
display_fields = {
    "Group": "dependency_group",
    "Name": "package_name",
    "Version": "package_version",
    "ID": "id",
    "Withdrawn": "withdrawn",
    "Fix Versions": "fixed_in",
    "Link": "link",
}


def get_vulnerabilities(
    *,
    poetry_packages: dict[Package, PoetryPackage],
    vulnerable_packages: Iterable[VulnerablePackage]
) -> list[Vulnerability]:
    """Combine fields from each vulnerablity and poetry dependency group."""
    vulnerabilities = []
    for vulnerable in vulnerable_packages:

        package_name = vulnerable.name
        package_version = vulnerable.version
        package = Package(name=package_name, version=package_version)

        for vulnerability in vulnerable.vulnerabilities:
            vulnerabilities.append(
                Vulnerability(
                    package_name=package_name,
                    package_version=package_version,
                    dependency_group=poetry_packages[package].category,
                    id=vulnerability["id"],
                    details=vulnerability["details"],
                    link=vulnerability["link"],
                    fixed_in=", ".join(vulnerability["fixed_in"]),
                    withdrawn=vulnerability["withdrawn"],
                )
            )

    return vulnerabilities


def format_vulnerabilities(vulnerabilities: Collection[Vulnerability]) -> str:
    rows = [
        {
            display_name: getattr(vulnerability, field_name)
            for display_name, field_name in display_fields.items()
        }
        for vulnerability in vulnerabilities
    ]
    assert len(vulnerabilities) == len(rows)

    content = tabulate(rows, headers="keys")
    return content


def is_all_withdrawn(vulnerabilities: Iterable[Vulnerability]) -> bool:
    return all(vulnerability.withdrawn is not None for vulnerability in vulnerabilities)
