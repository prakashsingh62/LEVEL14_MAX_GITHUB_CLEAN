@echo off
REM ============================================
REM   LEVEL-14 — Master Launcher (Windows)
REM ============================================

echo.
echo  Setting PYTHONPATH to project root...
set PYTHONPATH=%cd%

echo  Activating virtual environment...
call venv\Scripts\activate

echo.
echo  Starting LEVEL-14 Backend Server...
echo  ------------------------------------
python -m core.main

echo.
pause
