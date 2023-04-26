[
![Docs](https://img.shields.io/badge/read-docs-success)
](https://materials-data-science-and-informatics.github.io/dev-utils)
[
![CI](https://img.shields.io/github/actions/workflow/status/Materials-Data-Science-and-Informatics/dev-utils/ci.yml?branch=main&label=CI)
](https://github.com/Materials-Data-Science-and-Informatics/dev-utils/actions?query=workflow:ci)
[
![Docs Coverage](https://materials-data-science-and-informatics.github.io/dev-utils/main/interrogate_badge.svg)
](https://materials-data-science-and-informatics.github.io/dev-utils)
[
![Test Coverage](https://materials-data-science-and-informatics.github.io/dev-utils/main/coverage_badge.svg)
](https://materials-data-science-and-informatics.github.io/dev-utils/main/coverage)

<!-- --8<-- [start:abstract] -->
# dev-utils

Helper utilities for development, used from other repositories.

<!-- --8<-- [end:abstract] -->
<!-- --8<-- [start:quickstart] -->

## Getting Started

### update-codemeta

The `update-codemeta` pre-commit hook uses `codemetapy` to generate or update
a `codemeta.json` based on metadata in your `pyproject.toml`.

You can use it by adding the following snippet to your `.pre-commit-config.yaml`:

```yaml
...
  - repo: https://github.com/Materials-Data-Science-and-Informatics/dev-utils
    rev: 'LATEST_VERSION_TAG'  # <- replace with latest release tag or commit hash
    hooks:
      - id: update-codemeta
        files: ^pyproject.toml$
...
```
<!-- --8<-- [end:quickstart] -->

**You can find more information on using and contributing to this repository in the
[documentation](https://materials-data-science-and-informatics.github.io/dev-utils).**

<!-- --8<-- [start:citation] -->

## How to Cite

If you want to cite this project in your scientific work,
please use the [citation file](https://citation-file-format.github.io/)
in the [repository](https://github.com/Materials-Data-Science-and-Informatics/dev-utils/blob/main/CITATION.cff).

<!-- --8<-- [end:citation] -->
<!-- --8<-- [start:acknowledgements] -->

## Acknowledgements

We kindly thank all
[authors and contributors](https://materials-data-science-and-informatics.github.io/dev-utils/main/credits).


<!-- --8<-- [end:acknowledgements] -->
