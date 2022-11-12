# ko-poetry-audit-plugin

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![formatter](https://img.shields.io/badge/%20formatter-docformatter-fedcba.svg)](https://github.com/PyCQA/docformatter)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)
[![linting: pylint](https://img.shields.io/badge/linting-pylint-yellowgreen)](https://github.com/PyCQA/pylint)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)

To check known vulnerabilities from `poetry.lock`.

Inspired by [pypa/pip-audit](https://github.com/pypa/pip-audit), this adds `audit` command tip [`poetry`](https://python-poetry.org/docs/), for checking vulnerabilities of packages found in `poetry.lock`.

Vulnerability reports are sourced from Python Packaging Advisory Database (https://github.com/pypa/advisory-database) using [JSON API](https://warehouse.pypa.io/api-reference/json.html).

## Installation

Please follow poetry [Using Plugins](https://python-poetry.org/docs/plugins/#using-plugins) for installation.
```
% poetry self add ko-poetry-audit-plugin
```

To integrate with [`pre-commit`](https://pre-commit.com), trigger scan whenever `poetry.lock` is commit:
```yaml
  - repo: https://github.com/koyeung/ko-poetry-audit-plugin.git
    rev: 0.3.0
    hooks:
      - id: poetry-audit
```

**Note** by default, it scans for `main` and `dev` dependencies groups only.


## Usage

To check for `main` group:

```
% poetry audit
No known vulnerabilities found
```

To include packages in `dev` group:
```
% poetry audit --with dev
Found vulnerabilities
Group    Name    Version    ID                   Withdrawn    Fix Versions    Link
-------  ------  ---------  -------------------  -----------  --------------  -------------------------------------------------
dev      py      1.11.0     GHSA-w596-4wvx-j9j6                               https://osv.dev/vulnerability/GHSA-w596-4wvx-j9j6
dev      py      1.11.0     PYSEC-2022-42969                                  https://osv.dev/vulnerability/PYSEC-2022-42969
% echo $?
1
```

To show more details:
```
% poetry audit --with dev -vv
[ko_poetry_audit_plugin.auditor] get packages list from dependencies groups={'main', 'dev'}
[ko_poetry_audit_plugin.pypi_warehouse] package.name='boto3', package.version='1.26.8': no vulnerabilities found
[ko_poetry_audit_plugin.pypi_warehouse] package.name='jmespath', package.version='1.0.1': no vulnerabilities found
[ko_poetry_audit_plugin.pypi_warehouse] package.name='botocore', package.version='1.29.8': no vulnerabilities found
[ko_poetry_audit_plugin.pypi_warehouse] package.name='six', package.version='1.16.0': no vulnerabilities found
[ko_poetry_audit_plugin.pypi_warehouse] package.name='python-dateutil', package.version='2.8.2': no vulnerabilities found
[ko_poetry_audit_plugin.pypi_warehouse] package.name='s3transfer', package.version='0.6.0': no vulnerabilities found
[ko_poetry_audit_plugin.pypi_warehouse] package.name='py', package.version='1.11.0': vulnerabilities found
[ko_poetry_audit_plugin.pypi_warehouse] package.name='urllib3', package.version='1.26.12': no vulnerabilities found
Found vulnerabilities
Group    Name    Version    ID                   Withdrawn    Fix Versions    Link
-------  ------  ---------  -------------------  -----------  --------------  -------------------------------------------------
dev      py      1.11.0     GHSA-w596-4wvx-j9j6                               https://osv.dev/vulnerability/GHSA-w596-4wvx-j9j6
dev      py      1.11.0     PYSEC-2022-42969                                  https://osv.dev/vulnerability/PYSEC-2022-42969
```

## Exit codes
`poetry audit` exits with non-zero code, unless all vulnerabilities found have been withdrawn.

**Note** only packages found on `pypi` could be checked.

## Licensing
`poetry audit` plugin is licensed under the Apache 2.0 License.
