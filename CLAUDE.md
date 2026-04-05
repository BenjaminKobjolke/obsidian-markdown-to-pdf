# Obsidian Markdown to PDF — Development Guide

## Project Overview

Python CLI tool to convert Obsidian-flavored markdown to PDF. Uses `markdown` + `obsidian-media` for parsing and `weasyprint` for PDF rendering.

## Tech Stack

- Python 3.12, managed with `uv`
- `markdown` + `obsidian-media` for MD→HTML
- `weasyprint` for HTML→PDF
- `python-frontmatter` for YAML stripping
- `ruff` + `mypy` for linting/type checking
- `pytest` for testing

## Coding Rules

- `pyproject.toml` is single source of truth — no scattered config files
- Max 300 lines per file
- snake_case for files/functions, PascalCase for classes, UPPER_SNAKE_CASE for constants
- Type hints on all public APIs
- Structured logging via `logging` module (no print)
- Centralize string constants in `src/constants.py`
- DRY — no code duplication
- No god classes — single responsibility per class
- Tests are mandatory — use pytest
- Validate input at system boundaries

## Batch Files

- `start.bat` — run the tool
- `install.bat` — initial setup
- `update.bat` — update dependencies
- `tools/run_tests.bat` — run test suite
- `tools/run_integration_tests.bat` — run integration tests
