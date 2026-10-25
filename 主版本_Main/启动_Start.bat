@echo off
rem BaseConverter main visual edition launcher (PySide6 + QML).
rem
rem Picks a Python 3.9+ interpreter that already has PySide6. If none has the
rem dependency, it offers to install requirements.txt into the first
rem suitable interpreter. Pass --auto to skip the confirmation prompt.
setlocal EnableExtensions
cd /d "%~dp0"
set "APP=main.py"
set "AUTO="
if /i "%~1"=="--auto" set "AUTO=1"
set "PY="
set "PYW="
set "BASEPY="
set "BASE_PYW="

call :check_python
if defined PY goto :launch
call :check_py
if defined PY goto :launch
if not defined BASEPY goto :no_python
goto :install_pyside

:check_python
where python >nul 2>nul
if errorlevel 1 exit /b 0
python -c "import sys; raise SystemExit(0 if sys.version_info >= (3, 9) else 3)" >nul 2>nul
if errorlevel 1 exit /b 0
if not defined BASEPY (
    set "BASEPY=python"
    where pythonw >nul 2>nul
    if not errorlevel 1 (set "BASE_PYW=pythonw") else (set "BASE_PYW=python")
)
python -c "import PySide6" >nul 2>nul
if not errorlevel 1 (
    set "PY=python"
    set "PYW=pythonw"
)
exit /b 0

:check_py
where py >nul 2>nul
if errorlevel 1 exit /b 0
py -3 -c "import sys; raise SystemExit(0 if sys.version_info >= (3, 9) else 3)" >nul 2>nul
if errorlevel 1 exit /b 0
if not defined BASEPY (
    set "BASEPY=py -3"
    where pyw >nul 2>nul
    if not errorlevel 1 (set "BASE_PYW=pyw -3") else (set "BASE_PYW=py -3")
)
py -3 -c "import PySide6" >nul 2>nul
if not errorlevel 1 (
    set "PY=py -3"
    set "PYW=pyw -3"
)
exit /b 0

:install_pyside
echo.
echo The visual edition needs PySide6 (Qt 6) for the QML interface.
if not defined AUTO (
    choice /c YN /n /m "Install PySide6 now with pip? [Y/N] "
    if errorlevel 2 goto :manual_install
)
echo.
echo Installing PySide6. This may take a few minutes...
%BASEPY% -m pip install -r "requirements.txt"
if errorlevel 1 goto :manual_install
%BASEPY% -c "import PySide6" >nul 2>nul
if errorlevel 1 goto :manual_install
set "PY=%BASEPY%"
set "PYW=%BASE_PYW%"
goto :launch

:manual_install
echo.
echo Automatic installation failed. Install the dependency manually:
echo   %BASEPY% -m pip install -r requirements.txt
pause
exit /b 1

:launch
start "" %PYW% "%APP%"
exit /b 0

:no_python
echo.
echo Python 3.9 or newer was not found.
echo Install Python 3.12 or 3.13 from:
echo   https://www.python.org/downloads/windows/
echo During installation, enable "Add python.exe to PATH".
start "" "https://www.python.org/downloads/windows/"
pause
exit /b 1
