import pytest

from ko_poetry_audit_plugin.packages import Package
from ko_poetry_audit_plugin.pypi_warehouse import _get_packages_metadata


@pytest.mark.asyncio
@pytest.mark.usefixtures(
    "sampleproject_response", "django_response", "no_such_package_response"
)
async def test_get_packages_metadata():

    sampleproject = Package(name="sampleproject", version="1.0.0")
    django = Package(name="Django", version="3.0.2")
    no_such_package = Package(name="no_such_package", version="1.0.0")

    packages = [sampleproject, django, no_such_package]

    result = await _get_packages_metadata(packages)

    assert len(result) == 3

    by_package = {
        Package(name=package.name, version=package.version): package
        for package in result
    }

    assert by_package[sampleproject].metadata["vulnerabilities"] == []
    assert by_package[django].metadata[
        "vulnerabilities"
    ], "should have some vulnerabilities"
    assert by_package[no_such_package].metadata is None
