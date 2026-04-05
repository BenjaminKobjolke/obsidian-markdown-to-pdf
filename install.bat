@echo off
echo ========================================
echo  Obsidian Markdown to PDF - Initial Setup
echo ========================================
echo.

:: Check if uv is installed
where uv >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo ERROR: uv is not installed or not in PATH
    echo Please install uv first: https://docs.astral.sh/uv/getting-started/installation/
    pause
    exit /b 1
)

echo [1/2] Creating virtual environment and installing dependencies...
uv sync --all-extras
if %ERRORLEVEL% neq 0 (
    echo ERROR: Failed to sync dependencies
    pause
    exit /b 1
)

echo.
echo [2/2] Running tests...
uv run pytest tests/ -q
if %ERRORLEVEL% neq 0 (
    echo WARNING: Some tests failed
)

echo.
echo ========================================
echo  Setup complete!
echo ========================================
echo.
echo Usage: start.bat --input "path/to/file.md" --output "output.pdf"
echo.
pause
