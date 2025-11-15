@echo off
REM Uutistenlukija - Windows käynnistin
REM Tuplaklikkaus-yhteensopiva versio

REM Siirry projektikansioon (yksi taso ylöspäin)
cd /d "%~dp0.."

echo.
echo ╔══════════════════════════════════════╗
echo ║   🗞️  UUTISTENLUKIJA - WINDOWS  🗞️  ║
echo ╚══════════════════════════════════════╝
echo.
echo Kaynnistetaan...
echo.

REM Tarkista onko PowerShell saatavilla
where powershell >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Virhe: PowerShell ei loytynyt!
    echo.
    echo Yritetaan Python-versiota...
    python kaynnista_helppo.py
    if %ERRORLEVEL% NEQ 0 (
        echo.
        echo ❌ Myos Python-versio epaonnistui!
        echo.
        echo Varmista etta Python on asennettu.
    )
    echo.
    pause
    exit /b 1
)

REM Käynnistä PowerShell TUI (windows-kansiossa)
powershell -ExecutionPolicy Bypass -NoExit -File "%~dp0kaynnista_tui.ps1"

REM Ikkuna pysyy auki PowerShell TUI:n ansiosta (-NoExit)
