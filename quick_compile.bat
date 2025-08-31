@echo off
echo ================================================
echo    Quick Feedback Compilation
echo ================================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    pause
    exit /b 1
)

echo Running compilation script...
python compile_feedback.py

echo.
echo Done! Check feedback.exe if compilation was successful.
pause