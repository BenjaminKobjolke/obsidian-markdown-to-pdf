@echo off
echo ========================================
echo  Obsidian Markdown to PDF - Update
echo ========================================
echo.

where uv >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo ERROR: uv is not installed or not in PATH
    exit /b 1
)

echo [1/3] Updating dependencies...
uv lock --upgrade
uv sync --all-extras
if %ERRORLEVEL% neq 0 (
    echo ERROR: Failed to update dependencies
    pause
    exit /b 1
)

echo.
echo [2/3] Linting...
uv run ruff check .
uv run ruff format --check .

echo.
echo [3/3] Running tests...
uv run pytest tests/ -q

echo.
echo ========================================
echo  Update complete!
echo ========================================
pause
