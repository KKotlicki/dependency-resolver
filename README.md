# Dependency Resolver

A Python package that resolves dependencies defined in a JSON file and prints the full dependency graph in a human-readable format.

## Author

**Konrad Kotlicki**

contact: [konrad.kotlicki@gmail.com](mailto:konrad.kotlicki@gmail.com)

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
  - [Command-Line Options](#command-line-options)
- [Examples](#examples)
- [Project Structure](#project-structure)
- [Development](#development)
- [Continuous Integration](#continuous-integration)

## Introduction

This project is designed to parse a JSON file containing package dependencies and reconstruct the full dependency graph.

## Features

- Parses dependencies from a JSON file.
- Resolves and reconstructs the full dependency graph.
- Prints the graph in a human-readable format.
- Handles circular dependencies gracefully.
- Includes thorough unit tests with high coverage.
- Utilizes pre-commit hooks for code quality.
- Continuous Integration with GitHub Actions.
- Customizable indentation and logging levels.
- Generates automated documentation with Sphinx.

## Installation

```bash
pip install .
```

## Usage

```bash
python -m dep_resolver <path_to_dependencies.json> [OPTIONS]
```

### Command-Line Options

- `--log-level`: Set the logging level (`DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`). Default is `INFO`.
- `--indent-size`: Set the indentation size for output. Default is `4`.

Example:

```bash
python -m dep_resolver tests/test_data/dependencies.json --log-level DEBUG --indent-size 2
```

## Examples

Given a `dependencies.json` file:

```json
{
    "pkg1": ["pkg2", "pkg3"],
    "pkg2": ["pkg3"],
    "pkg3": []
}
```

Running the command:

```bash
python -m dep_resolver dependencies.json
```

Produces:

```markdown
- pkg1
    - pkg2
        - pkg3
    - pkg3
- pkg2
    - pkg3
- pkg3

```

## Project Structure

<!-- PROJECT STRUCTURE START -->

```plaintext
dep-resolver/
├── .github/
│   └── workflows/
│       └── ci.yml
├── docs/
│   ├── build/
│   ├── source/
│   │   ├── conf.py
│   │   ├── dep_resolver.rst
│   │   ├── index.rst
│   │   └── modules.rst
│   ├── Makefile
│   └── make.bat
├── src/
│   └── dep_resolver/
│       ├── __init__.py
│       ├── __main__.py
│       ├── cli.py
│       ├── printer.py
│       └── resolver.py
├── tests/
│   ├── test_data/
│   ├── __init__.py
│   ├── test_cli.py
│   ├── test_printer.py
│   └── test_resolver.py
├── .gitignore
├── .pre-commit-config.yaml
├── MANIFEST.in
├── README.md
├── generate_project_structure.py
├── pyproject.toml
├── requirements-dev.txt
├── requirements.txt
├── setup.cfg
└── setup.py
```

<!-- PROJECT STRUCTURE END -->

## Development

### Development Tools Installation

Install development libraries and pre-commit hooks to ensure code quality before each commit:

```bash
pip install -e .[dev]
pre-commit install
```

### Linting and Formatting

- Linting: `flake8 src/ tests/`
- Formatting: `black src/ tests/`

### Type Checking

Run static type checks using `mypy`:

- `mypy src/`

### Testing

Run tests using `pytest`:

```bash
pytest
```

Generate a detailed coverage report as an HTML document in `./htmlcov/index.html`:

```bash
pytest --cov=dep_resolver --cov-report=html tests/
```

### Generating Documentation

Generate HTML documentation using Sphinx:

```bash
cd docs
make html
```

Open `docs/build/html/index.html` in your web browser to view the documentation.

## Continuous Integration

The project uses GitHub Actions for Continuous Integration. The workflow is defined in `.github/workflows/ci.yml` and runs tests, linting, and formatting checks on each push and pull request. Coverage reports are generated and stored as artifacts within the GitHub environment.
