@echo off
title Push Project to GitHub Repository (CG-Blender)
cls

echo =====================================================================
echo       Pushing 3D Game Environment Optimization to GitHub
echo       Repository: https://github.com/panchaksharayya12/CG-Blender.git
echo =====================================================================
echo.

echo [1/3] Checking Git Status...
git status

echo.
echo [2/3] Checking Remote Configuration...
git remote -v

echo.
echo [3/3] Pushing to GitHub (Branch: main)...
echo.
echo Note: If Git Credential Manager pops up, click "Sign in with your browser"
echo to authorize pushing to github.com/panchaksharayya12/CG-Blender.
echo.

git push -u origin main

if %ERRORLEVEL% EQU 0 (
    echo.
    echo =====================================================================
    echo [SUCCESS] Whole project and animations pushed to GitHub!
    echo View your repository online at:
    echo https://github.com/panchaksharayya12/CG-Blender
    echo =====================================================================
) else (
    echo.
    echo =====================================================================
    echo [NOTICE] If GitHub requested authentication, you can also paste a
    echo GitHub Personal Access Token (PAT) when prompted.
    echo =====================================================================
)

echo.
pause
