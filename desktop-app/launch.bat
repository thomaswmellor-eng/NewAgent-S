@echo off
echo ====================================
echo   Lancement Agent S3 Desktop
echo ====================================
echo.

REM Vérifier si node_modules existe
if not exist "node_modules" (
    echo [INFO] Premiere execution detectee
    echo Installation des dependances...
    echo.
    call setup.bat
    if %ERRORLEVEL% NEQ 0 exit /b 1
)

echo Lancement de l'application...
echo.
call npm start
