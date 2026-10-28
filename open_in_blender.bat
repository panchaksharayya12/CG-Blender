@echo off
title Open Game Environment in Blender 5.0
cls

echo =====================================================================
echo       Opening 3D Game Environment in Blender 5.0...
echo =====================================================================
echo.

if exist "C:\Program Files\Blender Foundation\Blender 5.0\blender.exe" (
    start "" "C:\Program Files\Blender Foundation\Blender 5.0\blender.exe" "%~dp0game_environment.blend"
) else (
    echo [INFO] Opening with default system Blender association...
    start "" "%~dp0game_environment.blend"
)

echo Blender has been launched!
