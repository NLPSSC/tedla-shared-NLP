@echo off
title TEDLA Hypertension NLP Pipeline
echo.
echo    ========================================
echo      TEDLA Hypertension NLP Pipeline
echo    ========================================
echo.
echo    Starting launcher...
echo.

:: Try python, then python3, then py
where python >nul 2>nul
if %errorlevel%==0 (
    python "%~dp0launcher.py"
    goto :end
)

where python3 >nul 2>nul
if %errorlevel%==0 (
    python3 "%~dp0launcher.py"
    goto :end
)

where py >nul 2>nul
if %errorlevel%==0 (
    py "%~dp0launcher.py"
    goto :end
)

echo.
echo ERROR: Python is not installed or not in your PATH.
echo Please install Python from https://www.python.org/downloads/
echo Make sure to check "Add Python to PATH" during installation.
echo.
pause

:end
