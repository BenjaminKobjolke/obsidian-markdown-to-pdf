@echo off
where uv >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo ERROR: uv is not installed or not in PATH
    echo Please install uv first: https://docs.astral.sh/uv/getting-started/installation/
    exit /b 1
)

if exist "C:\msys64\ucrt64\bin" set PATH=C:\msys64\ucrt64\bin;%PATH%

uv run python main.py %*
