import pytest


@pytest.fixture
def sampleproject_response(httpx_mock, test_data):
    httpx_mock.add_response(
        url="https://pypi.org/pypi/sampleproject/1.0.0/json",
        text=(test_data / "sampleproject_1.2.0.txt").read_text(),
    )


@pytest.fixture
def django_response(httpx_mock, test_data):
    httpx_mock.add_response(
        url="https://pypi.org/pypi/Django/3.0.2/json",
        text=(test_data / "django_3.0.2.txt").read_text(),
    )


@pytest.fixture
def no_such_package_response(httpx_mock, test_data):
    httpx_mock.add_response(
        url="https://pypi.org/pypi/no_such_package/1.0.0/json",
        text=(test_data / "no_such_package_1.0.0.txt").read_text(),
        status_code=404,
    )
