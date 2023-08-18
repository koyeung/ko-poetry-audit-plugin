# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]

## [0.8.0a1] - 2023-08-18
* update dependencies versions
* fix for tox v4

## [0.8.0a0] - 2023-06-01
### Changed
* update dependencies versions
* no auto run of docformatter by pre-commit

## [0.7.0] - 2022-12-10
### Changed
* update dependencies with poetry 1.3.0
* adapt to tox 4
* reduce relying on `pre-commit` in ci.

## [0.6.0] - 2022-11-14
### Changed
* revise readme
* remove pre-commit ci config
* add Python 3.9 support
* add tox-ini-fmt to `pre-commit` config
* `.pre-commit-config.yaml` - add hook `poetry-audit`

## [0.5.0] - 2022-11-12
### Changed
* `.pre-commit-hooks.yaml` - pass `-vv` to `args`
* log message if package/version are skipped.

## [0.4.0] - 2022-11-11
### Add
* update `README.md` on setup as pre-commit hook.

## [0.3.0] - 2022-11-11
### Add
* add `.pre-commit-hooks.yaml`

## [0.2.0] - 2022-11-11
### Add
* initial project setup
* implement `audit` command


[Unreleased]: https://github.com/koyeung/ko-poetry-audit-plugin/compare/main...HEAD
[0.8.0a1]: https://github.com/koyeung/ko-poetry-audit-plugin/releases/tag/0.8.0a1
[0.8.0a0]: https://github.com/koyeung/ko-poetry-audit-plugin/releases/tag/0.8.0a0
[0.7.0]: https://github.com/koyeung/ko-poetry-audit-plugin/releases/tag/0.7.0
[0.6.0]: https://github.com/koyeung/ko-poetry-audit-plugin/releases/tag/0.6.0
[0.5.0]: https://github.com/koyeung/ko-poetry-audit-plugin/releases/tag/0.5.0
[0.4.0]: https://github.com/koyeung/ko-poetry-audit-plugin/releases/tag/0.4.0
[0.3.0]: https://github.com/koyeung/ko-poetry-audit-plugin/releases/tag/0.3.0
[0.2.0]: https://github.com/koyeung/ko-poetry-audit-plugin/releases/tag/0.2.0
