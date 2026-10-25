@echo off
rem BaseConverter single-file edition launcher (tkinter + stdlib).
rem
rem Starts the application with the first usable Python 3 interpreter. If no
rem interpreter is found, it offers to install Python through winget. Pass
rem --auto to skip the confirmation prompt.
setlocal EnableExtensions
cd /d "%~dp0"
set "APP=main.py"
set "AUTO="
if /i "%~1"=="--auto" set "AUTO=1"
set "ENV_MISSING="

rem Console interpreters can be probed reliably: the process waits and the
rem exit code reports whether Python 3.8+ and tkinter are available. The
rem windowless variant is used afterwards to start the application.
where py >nul 2>nul
if not errorlevel 1 (
    py -3 -c "import sys, tkinter; raise SystemExit(0 if sys.version_info >= (3, 8) else 3)" >nul 2>nul
    if errorlevel 1 (
        set "ENV_MISSING=1"
    ) else (
        call :launch_pyw
        if not errorlevel 1 exit /b 0
        start "" py -3 "%APP%"
        exit /b 0
    )
)

where python >nul 2>nul
if not errorlevel 1 (
    python -c "import sys, tkinter; raise SystemExit(0 if sys.version_info >= (3, 8) else 3)" >nul 2>nul
    if errorlevel 1 (
        set "ENV_MISSING=1"
    ) else (
        call :launch_pythonw
        if not errorlevel 1 exit /b 0
        start "" python "%APP%"
        exit /b 0
    )
)

rem GUI-only interpreters: start them and let main.py report a missing Tk toolkit.
call :launch_pyw
if not errorlevel 1 exit /b 0
call :launch_pythonw
if not errorlevel 1 exit /b 0

if defined ENV_MISSING goto :bad_environment

echo.
echo Python 3 was not found on this system.
goto :install

:bad_environment
echo.
echo Python was found, but Python 3.8 or newer with the Tk toolkit is required.
echo A complete Python 3.13 installation can be added alongside the existing one.

:install
where winget >nul 2>nul
if errorlevel 1 goto :manual
if not defined AUTO (
    choice /c YN /n /m "Install Python 3 automatically with winget? [Y/N] "
    if errorlevel 2 goto :manual
)

echo.
echo Installing Python 3 with winget. This may take several minutes...
winget install --id Python.Python.3.13 -e --scope user --accept-package-agreements --accept-source-agreements
if errorlevel 1 (
    echo Retrying without the user-scope option...
    winget install --id Python.Python.3.13 -e --accept-package-agreements --accept-source-agreements
)
if errorlevel 1 (
    echo Trying Python 3.12...
    winget install --id Python.Python.3.12 -e --accept-package-agreements --accept-source-agreements
)

call :launch_installed
if not errorlevel 1 exit /b 0

echo.
echo Python could not be installed or started automatically.
echo Install Python 3.8 or newer from https://www.python.org/downloads/windows/
pause
exit /b 1

:manual
echo.
echo Install Python 3.8 or newer from:
echo   https://www.python.org/downloads/windows/
echo During installation, enable "Add python.exe to PATH" and "tcl/tk and IDLE".
start "" "https://www.python.org/downloads/windows/"
pause
exit /b 1

:launch_pyw
where pyw >nul 2>nul
if errorlevel 1 exit /b 1
start "" pyw -3 "%APP%"
exit /b 0

:launch_pythonw
where pythonw >nul 2>nul
if errorlevel 1 exit /b 1
start "" pythonw "%APP%"
exit /b 0

:launch_installed
rem winget does not refresh PATH in the current console, so look in the
rem standard per-user and machine-wide installation directories.
for /d %%D in ("%LOCALAPPDATA%\Programs\Python\Python3*") do (
    if exist "%%~fD\python.exe" (
        "%%~fD\python.exe" -c "import sys, tkinter; raise SystemExit(0 if sys.version_info >= (3, 8) else 3)" >nul 2>nul
        if not errorlevel 1 (
            if exist "%%~fD\pythonw.exe" (
                start "" "%%~fD\pythonw.exe" "%APP%"
            ) else (
                start "" "%%~fD\python.exe" "%APP%"
            )
            exit /b 0
        )
    )
)
for /d %%D in ("%ProgramFiles%\Python3*") do (
    if exist "%%~fD\python.exe" (
        "%%~fD\python.exe" -c "import sys, tkinter; raise SystemExit(0 if sys.version_info >= (3, 8) else 3)" >nul 2>nul
        if not errorlevel 1 (
            if exist "%%~fD\pythonw.exe" (
                start "" "%%~fD\pythonw.exe" "%APP%"
            ) else (
                start "" "%%~fD\python.exe" "%APP%"
            )
            exit /b 0
        )
    )
)
exit /b 1
