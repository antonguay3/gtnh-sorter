@echo off
cd /d "%~dp0core"

echo [GTNH Sorter] Checking virtual environment...
if exist ".venv\Scripts\python.exe" goto :check_libs

echo [GTNH Sorter] .venv not found or broken. Creating virtual environment...
python -m venv .venv

:check_libs
echo [GTNH Sorter] Checking required libraries...
.venv\Scripts\python.exe -c "import numpy" 2>nul
if not errorlevel 1 goto :launch

echo [GTNH Sorter] Installing required packages (Pillow, numpy, tqdm)...
.venv\Scripts\python.exe -m pip install --upgrade pip
.venv\Scripts\python.exe -m pip install Pillow numpy tqdm

:launch
echo [GTNH Sorter] Launching Search Item script...
echo --------------------------------------------------
.venv\Scripts\python.exe search_item.py

echo --------------------------------------------------
echo [GTNH Sorter] Application closed.
pause