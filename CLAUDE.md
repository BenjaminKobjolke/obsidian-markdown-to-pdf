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

> Source: `D:\GIT\BenjaminKobjolke\claude-code\coding-rules` (`COMMON_RULES.md` + `PYTHON_RULES.md`).
> Web/API-only rules (Jinja2, i18n, SQLAlchemy, async, Pydantic API validation) are omitted —
> this is a CLI markdown→PDF tool.

### Common (all languages)

- **DRY** — no code duplication; extract shared logic into helpers/base abstractions, constants for repeated values
- **Derive, don't duplicate** — when one value determines another, pass only the determinant and derive the rest (single source of truth for parameters); keep derivation cheap, pure, exhaustive
- **Use objects for related values** — bundle related params into a DTO/Settings/Config instead of many parameters
- **No bag-of-keys returns at module boundaries** — public methods return typed objects (DTO/value object/model), never raw dicts keyed by strings; distinguish absent (`None`) from empty
- **Reuse existing models** before inventing new array shapes — grep for the table/key/column first
- **Tests pin the shape before refactor** — write a characterization test first, green it, then refactor
- **TDD** — write tests, confirm they fail, implement, confirm they pass
- **Integration tests mandatory** — in addition to unit tests
- **Prefer type-safe values** — typed DTOs, enums, `Literal`, typed settings over stringly-typed
- **Centralize string constants** in `src/constants.py` — no scattered raw strings
- **Confirm dependency versions** with the user before adding any new package
- **Centralized error handling + logging** — structured logging, appropriate levels, context in messages
- **Input validation at boundaries** — never trust external data (CLI args, file input); fail fast
- **Max 300 lines per file** — split by domain; exceptions for generated/config/test files
- **Naming**: files/functions `snake_case`, classes `PascalCase`, constants `UPPER_SNAKE_CASE`
- **Security baseline** — never commit secrets, escape output, keep deps updated
- **No god classes** — single responsibility; warning signs: >5 public methods, >4 ctor deps, mixed domains
- **Self-describing classes** — classes declare their own fields via contract (Protocol/ABC/dataclass metadata); never hardcode field lists in consumers
- **README.md mandatory** — name, description, setup, usage, dependencies
- **Reusable tooling** — check the language's `*_setup_files/` folder before building project-specific scripts

### Python (uv)

- **`pyproject.toml` is single source of truth** — no scattered config files; commit `uv.lock`; pin Python version
- **ruff + mypy** — ruff handles lint + formatting; mypy for typing; run `ruff check`, `ruff format --check`, `mypy`
- **Type hints on all public APIs** — typed params + return types; use `Sequence`/`Mapping`/`Protocol`/`TypedDict`/`Literal`; avoid `Any` except at I/O boundaries
- **Centralized env-driven settings** — single settings module/dataclass, no magic values scattered via `os.getenv()`
- **Tests mandatory, fast, isolated** — pytest; no network in unit tests; tmp dirs/fixtures, no machine-state reliance
- **`spec=` with MagicMock** — `MagicMock(spec=RealClass)` to catch interface mismatches; mock methods as methods (`mock.get_body.return_value`), not fake attributes
- **Structured logging via `AppLogger`** (`app_logger.py`) wrapping `logging`/`structlog` — feature code calls `AppLogger`, never `logging.getLogger(...)` or `print()` directly (single off/level switch)
- **Self-describing classes** — Protocol with abstract method (simple cases) or dataclass field metadata (declarative per-field)

## Batch Files

- `start.bat` — run the tool
- `install.bat` — initial setup
- `update.bat` — update dependencies
- `tools/run_tests.bat` — run test suite
- `tools/run_integration_tests.bat` — run integration tests
- `tools/analyze_code.bat` — run cli-code-analyzer
- `tools/fix_ruff_issues.bat` — auto-fix Ruff issues

## Code Analysis

After implementing new features or making significant changes, run the code analysis:

```bash
powershell -Command "cd 'D:\GIT\BenjaminKobjolke\obsidian-markdown-to-pdf'; cmd /c '.\tools\analyze_code.bat'"
```

Fix any reported issues before committing.
