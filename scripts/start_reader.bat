@echo off
REM Uutislukija - Käynnistysskripti Windowsille

cd /d "%~dp0\.."

echo Uutislukija (HS ^& YLE)
echo ========================
echo.

REM Tarkista että virtuaaliympäristö on olemassa
if not exist "venv\Scripts\python.exe" (
    echo VIRHE: Python virtuaaliymparisto ei loydy!
    echo Aja ensin: python -m venv venv
    echo.
    pause
    exit /b 1
)

REM Käynnistä ohjelma
venv\Scripts\python.exe uutistenlukija.py

pause
