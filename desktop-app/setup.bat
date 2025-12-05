@echo off
echo ====================================
echo   Agent S3 Desktop - Setup
echo ====================================
echo.

REM Vérifier si Node.js est installé
where node >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [ERREUR] Node.js n'est pas installe!
    echo.
    echo Telechargez Node.js depuis: https://nodejs.org/
    echo Puis relancez ce script.
    pause
    exit /b 1
)

echo [OK] Node.js detecte:
node --version
echo.

REM Installer les dépendances
echo Installation des dependances npm...
echo.
call npm install

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [ERREUR] Installation echouee!
    pause
    exit /b 1
)

echo.
echo ====================================
echo   Installation terminee!
echo ====================================
echo.
echo Pour lancer l'app:
echo   npm start
echo.
echo Pour creer l'installateur .exe:
echo   npm run build:win
echo.
pause
