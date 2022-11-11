from ko_poetry_audit_plugin.packages import (
    Package,
    PoetryPackage,
    Vulnerability,
    VulnerablePackage,
)
from ko_poetry_audit_plugin.vulnerabilities import (
    format_vulnerabilities,
    get_vulnerabilities,
    is_all_withdrawn,
)


def test_get_vulnerabilities():
    poetry_packages = {
        Package(name="sampleproject", version="1.2.0"): PoetryPackage(
            name="sampleproject", version="1.2.0", category="main"
        ),
        Package(name="Django", version="3.0.2"): PoetryPackage(
            name="Django", version="3.0.2", category="main"
        ),
        Package(name="no_such_package", version="1.0.0"): PoetryPackage(
            name="no_such_package", version="1.0.0", category="main"
        ),
    }

    vulnerable_packages = [
        VulnerablePackage(
            name="Django",
            version="3.0.2",
            vulnerabilities=[
                {
                    "aliases": ["CVE-2021-3281"],
                    "details": "PYSEC-2021-9 details",
                    "fixed_in": ["2.2.18", "3.0.12", "3.1.6"],
                    "id": "PYSEC-2021-9",
                    "link": "https://osv.dev/vulnerability/PYSEC-2021-9",
                    "source": "osv",
                    "summary": None,
                    "withdrawn": None,
                },
                {
                    "aliases": ["CVE-2020-13596"],
                    "details": "GHSA-2m34-jcjv-45xf details",
                    "fixed_in": ["2.2.13", "3.0.7"],
                    "id": "GHSA-2m34-jcjv-45xf",
                    "link": "https://osv.dev/vulnerability/GHSA-2m34-jcjv-45xf",
                    "source": "osv",
                    "summary": None,
                    "withdrawn": None,
                },
            ],
        )
    ]

    result = get_vulnerabilities(
        poetry_packages=poetry_packages,
        vulnerable_packages=vulnerable_packages,
    )

    assert result == [
        Vulnerability(
            package_name="Django",
            package_version="3.0.2",
            dependency_group="main",
            id="PYSEC-2021-9",
            details="PYSEC-2021-9 details",
            link="https://osv.dev/vulnerability/PYSEC-2021-9",
            fixed_in="2.2.18, 3.0.12, 3.1.6",
            withdrawn=None,
        ),
        Vulnerability(
            package_name="Django",
            package_version="3.0.2",
            dependency_group="main",
            id="GHSA-2m34-jcjv-45xf",
            details="GHSA-2m34-jcjv-45xf details",
            link="https://osv.dev/vulnerability/GHSA-2m34-jcjv-45xf",
            fixed_in="2.2.13, 3.0.7",
            withdrawn=None,
        ),
    ]


def test_format_vulnerabilities():
    vulnerabilities = [
        Vulnerability(
            package_name="Django",
            package_version="3.0.2",
            dependency_group="main",
            id="PYSEC-2021-9",
            details="PYSEC-2021-9 details",
            link="https://osv.dev/vulnerability/PYSEC-2021-9",
            fixed_in="2.2.18, 3.0.12, 3.1.6",
            withdrawn=None,
        ),
        Vulnerability(
            package_name="Django",
            package_version="3.0.2",
            dependency_group="main",
            id="GHSA-2m34-jcjv-45xf",
            details="GHSA-2m34-jcjv-45xf details",
            link="https://osv.dev/vulnerability/GHSA-2m34-jcjv-45xf",
            fixed_in="2.2.13, 3.0.7",
            withdrawn=None,
        ),
    ]

    result = format_vulnerabilities(vulnerabilities)
    assert (
        result
        == """\
Group    Name    Version    ID                   Withdrawn    Fix Versions           Link
-------  ------  ---------  -------------------  -----------  ---------------------  -------------------------------------------------
main     Django  3.0.2      PYSEC-2021-9                      2.2.18, 3.0.12, 3.1.6  https://osv.dev/vulnerability/PYSEC-2021-9
main     Django  3.0.2      GHSA-2m34-jcjv-45xf               2.2.13, 3.0.7          https://osv.dev/vulnerability/GHSA-2m34-jcjv-45xf"""  # pylint: disable=line-too-long
    )


def test_is_all_withdrawn():
    vulnerabilities = [
        Vulnerability(
            package_name="Django",
            package_version="3.0.2",
            dependency_group="main",
            id="PYSEC-2021-9",
            details="PYSEC-2021-9 details",
            link="https://osv.dev/vulnerability/PYSEC-2021-9",
            fixed_in="2.2.18, 3.0.12, 3.1.6",
            withdrawn=None,
        ),
        Vulnerability(
            package_name="Django",
            package_version="3.0.2",
            dependency_group="main",
            id="GHSA-2m34-jcjv-45xf",
            details="GHSA-2m34-jcjv-45xf details",
            link="https://osv.dev/vulnerability/GHSA-2m34-jcjv-45xf",
            fixed_in="2.2.13, 3.0.7",
            withdrawn=None,
        ),
    ]

    assert not is_all_withdrawn(vulnerabilities)
