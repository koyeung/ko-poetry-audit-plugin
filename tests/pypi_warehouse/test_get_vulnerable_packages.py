import pytest

from ko_poetry_audit_plugin.packages import Package
from ko_poetry_audit_plugin.pypi_warehouse import get_vulnerable_packages


@pytest.mark.usefixtures("sampleproject_response", "django_response")
def test_get_vulnerable_packages():
    sampleproject = Package(name="sampleproject", version="1.0.0")
    django = Package(name="Django", version="3.0.2")

    packages = [sampleproject, django]

    result = get_vulnerable_packages(packages)

    assert len(result) == 1

    by_package = {
        Package(name=package.name, version=package.version): package
        for package in result
    }

    assert by_package[django].vulnerabilities, "should have some vulnerabilities"


@pytest.mark.usefixtures(
    "sampleproject_response", "django_response", "no_such_package_response"
)
def test_not_all_package_found():
    sampleproject = Package(name="sampleproject", version="1.0.0")
    django = Package(name="Django", version="3.0.2")
    no_such_package = Package(name="no_such_package", version="1.0.0")

    packages = [sampleproject, django, no_such_package]

    with pytest.raises(RuntimeError) as exc:
        get_vulnerable_packages(packages)

    assert (
        str(exc.value)
        == "failed to fetch info from pypi: package.name='no_such_package', package.version='1.0.0'"
    )
