@echo off
cd /d "%~dp0"

where pyw >nul 2>nul
if not errorlevel 1 (
    start "" pyw -3 main.py
    exit /b 0
)

where pythonw >nul 2>nul
if not errorlevel 1 (
    start "" pythonw main.py
    exit /b 0
)

where py >nul 2>nul
if not errorlevel 1 (
    start "" py -3 main.py
    exit /b 0
)

where python >nul 2>nul
if not errorlevel 1 (
    start "" python main.py
    exit /b 0
)

echo Python 3 not found, see README.md
pause
