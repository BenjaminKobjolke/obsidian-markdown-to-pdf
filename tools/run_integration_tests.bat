@echo off
where uv >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo ERROR: uv is not installed or not in PATH
    exit /b 1
)

uv run pytest tests/ -v -m integration
