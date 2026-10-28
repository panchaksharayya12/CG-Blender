@echo off
title Real-Time 3D Game Environment Optimization | Back-Face Culling
cls

echo =====================================================================
echo    Real-Time 3D Game Environment Optimization Using Back-Face Culling
echo =====================================================================
echo.

:: 1. Check Python installation
python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Python was not found in your system PATH!
    echo Please install Python 3.10 or higher from https://python.org
    echo and make sure to check "Add Python to PATH" during installation.
    pause
    exit /b 1
)

echo [1/3] Python detected:
python --version

:: 2. Check and install dependencies
echo.
echo [2/3] Checking dependencies...
pip install -r requirements.txt
if %ERRORLEVEL% NEQ 0 (
    echo [WARNING] Failed to install dependencies via pip. Attempting to continue...
)

:: 3. Check if 3D models exist, if not run Blender exporter if Blender is installed
echo.
echo [3/3] Checking 3D environment assets...
if not exist "models\building.obj" (
    echo Models not found. Checking for Blender to generate assets...
    if exist "C:\Program Files\Blender Foundation\Blender 5.0\blender.exe" (
        echo Generating 3D assets via Blender 5.0...
        "C:\Program Files\Blender Foundation\Blender 5.0\blender.exe" --background --python export_blender_assets.py
    ) else (
        echo Blender not detected at default location; using procedural fallbacks.
    )
) else (
    echo 3D assets ready in models/ folder.
)

echo.
echo =====================================================================
echo Launching 3D Simulation...
echo Controls:
echo   - [W, A, S, D] : Fly and move around
echo   - [Mouse]      : Look around
echo   - [C]          : Toggle Back-Face Culling ON/OFF
echo   - [M]          : Toggle Wireframe / Solid mode
echo   - [T]          : Toggle Heavy-Poly Stress Grid
echo   - [U]          : Toggle Uncapped FPS Benchmark
echo   - [Tab]        : Unlock / Lock mouse cursor
echo =====================================================================
echo.

python main.py

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [ERROR] The program terminated unexpectedly.
    pause
)
