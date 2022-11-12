import asyncio
import logging
from http import HTTPStatus
from typing import Any, Iterable

import httpx

from ko_poetry_audit_plugin import __version__

from .packages import Package, PypiPackage, VulnerablePackage

LOGGER = logging.getLogger(__name__)

_USER_AGENT = f"{__package__}/{__version__}"


async def _get_package_metadata(
    name: str, version: str, client: httpx.AsyncClient
) -> tuple[str, str, Any | None]:

    uri = f"/{name}/{version}/json"
    response = await client.get(uri)

    return (
        name,
        version,
        response.json() if response.status_code == HTTPStatus.OK else None,
    )


async def _get_packages_metadata(packages: Iterable[Package]) -> list[PypiPackage]:

    headers = {"user-agent": _USER_AGENT}

    async with httpx.AsyncClient(
        base_url="https://pypi.org/pypi", headers=headers, http2=True
    ) as client:
        coros = [
            asyncio.create_task(
                _get_package_metadata(
                    name=package.name, version=package.version, client=client
                )
            )
            for package in packages
        ]

        result = []
        for coro in asyncio.as_completed(coros):
            name, version, metadata = await coro
            result.append(PypiPackage(name=name, version=version, metadata=metadata))

        return result


def get_vulnerable_packages(
    packages: Iterable[Package],
) -> list[VulnerablePackage]:

    metadata = asyncio.run(_get_packages_metadata(packages))

    # packages contains vulnerabilities
    result = []
    for package in metadata:

        if package.metadata is None:
            raise RuntimeError(
                f"failed to fetch info from pypi: {package.name=}, {package.version=}"
            )

        if not (vulnerabilities := package.metadata["vulnerabilities"]):
            LOGGER.info(
                f"{package.name=}, {package.version=}: no vulnerabilities found"
            )
            continue

        LOGGER.warning(f"{package.name=}, {package.version=}: vulnerabilities found")
        result.append(
            VulnerablePackage(
                name=package.name,
                version=package.version,
                vulnerabilities=vulnerabilities,
            )
        )

    return result
