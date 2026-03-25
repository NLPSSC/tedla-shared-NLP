@echo off
title TEDLA Hypertension NLP Pipeline - Combine Output
echo.
echo    ====================================================
echo      TEDLA Hypertension NLP Pipeline - Combine Output
echo    ====================================================
echo.
echo    Starting combination of output databases...
echo.

:: Set the first argument as input_folder
set "input_folder=%~1"

:: Set the second argument as output_folder
set "output_folder=%~2"


:: Try python, then python3, then py
where python >nul 2>nul
if %errorlevel%==0 (
    set "python_cmd=python"
    goto :next_action
)

where python3 >nul 2>nul
if %errorlevel%==0 (
    set "python_cmd=python3"
    goto :next_action
)

where py >nul 2>nul
if %errorlevel%==0 (
    set "python_cmd=py"
    goto :next_action
)

:next_action


if defined python_cmd (
    "%python_cmd%" "hypertension-nlp\src\results\combine_output.py" --input "%input_folder%" --output "%output_folder%"
) else (
    echo ERROR: Python was not found on this system.
    exit /b 1
)

goto :end

echo.
echo ERROR: Python is not installed or not in your PATH.
echo Please install Python from https://www.python.org/downloads/
echo Make sure to check "Add Python to PATH" during installation.
echo.
pause

:end
