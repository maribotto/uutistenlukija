# Uutistenlukija - Windows PowerShell TUI
# Graafinen käyttöliittymä Windowsille

param(
    [string]$Action = ""
)

# Värit
function Write-Header {
    param([string]$Text)
    Write-Host $Text -ForegroundColor Cyan
}

function Write-Success {
    param([string]$Text)
    Write-Host $Text -ForegroundColor Green
}

function Write-Warning {
    param([string]$Text)
    Write-Host $Text -ForegroundColor Yellow
}

function Write-Error {
    param([string]$Text)
    Write-Host $Text -ForegroundColor Red
}

function Write-Info {
    param([string]$Text)
    Write-Host $Text -ForegroundColor White
}

# Piirrä laatikko
function Draw-Box {
    param(
        [string]$Title,
        [string[]]$Lines
    )

    $maxLength = ($Lines | Measure-Object -Maximum -Property Length).Maximum
    $width = [Math]::Max($maxLength + 4, $Title.Length + 4)

    Write-Host ""
    Write-Header ("╔" + ("═" * $width) + "╗")
    Write-Header ("║ " + $Title.PadRight($width - 2) + " ║")
    Write-Header ("╠" + ("═" * $width) + "╣")

    foreach ($line in $Lines) {
        Write-Info ("║ " + $line.PadRight($width - 2) + " ║")
    }

    Write-Header ("╚" + ("═" * $width) + "╝")
    Write-Host ""
}

# Päävalikko
function Show-Menu {
    Clear-Host

    Write-Host ""
    Draw-Box "🗞️  UUTISTENLUKIJA  🗞️" @(
        "Helsingin Sanomat & YLE",
        "Suomeksi puhuen"
    )

    Write-Host ""
    Write-Header "PÄÄVALIKKO:"
    Write-Host ""
    Write-Info "  1. 🚀 Käynnistä uutislukija"
    Write-Info "  2. ⚙️  Tarkista asennus"
    Write-Info "  3. 🧪 Aja testit"
    Write-Info "  4. 📖 Näytä ohjeet"
    Write-Info "  5. 🚪 Lopeta"
    Write-Host ""

    $choice = Read-Host "Valitse (1-5)"
    return $choice
}

# Käynnistä uutislukija
function Start-Reader {
    Clear-Host
    Write-Header "═══════════════════════════════════════"
    Write-Header "  🚀 KÄYNNISTETÄÄN UUTISLUKIJA"
    Write-Header "═══════════════════════════════════════"
    Write-Host ""

    Write-Info "Tarkistetään asennus ja käynnistetään..."
    Write-Host ""

    # Käynnistä kaynnista.py (projektijuuressa)
    $scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
    $projectDir = Split-Path -Parent $scriptDir
    & python "$projectDir\kaynnista.py"

    Write-Host ""
    Write-Success "✓ Uutislukija on käynnistetty"
    Write-Host ""
    Write-Host "Paina Enter palataksesi valikkoon..." -ForegroundColor Gray
    Read-Host
}

# Tarkista asennus
function Check-Installation {
    Clear-Host
    Write-Header "═══════════════════════════════════════"
    Write-Header "  ⚙️  ASENNUKSEN TILA"
    Write-Header "═══════════════════════════════════════"
    Write-Host ""

    $scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
    $projectDir = Split-Path -Parent $scriptDir

    # Tarkista venv
    if (Test-Path "$projectDir\venv") {
        Write-Success "✓ Virtuaaliympäristö"
    } else {
        Write-Error "✗ Virtuaaliympäristö"
    }

    # Tarkista Piper
    if (Test-Path "$projectDir\piper\piper.exe") {
        Write-Success "✓ Piper TTS"
    } else {
        Write-Error "✗ Piper TTS"
    }

    # Tarkista äänimalli
    if (Test-Path "$projectDir\fi_FI-asmo-medium.onnx") {
        Write-Success "✓ Suomenkielinen äänimalli"
    } else {
        Write-Error "✗ Suomenkielinen äänimalli"
    }

    Write-Host ""

    # Yhteenveto
    $venvOk = Test-Path "$projectDir\venv"
    $piperOk = Test-Path "$projectDir\piper\piper.exe"
    $modelOk = Test-Path "$projectDir\fi_FI-asmo-medium.onnx"

    if ($venvOk -and $piperOk -and $modelOk) {
        Write-Success "✅ Kaikki asennettu!"
        Write-Info "   Voit käynnistää uutislukijan valinnalla 1"
    } else {
        Write-Warning "⚠️  Puuttuvia komponentteja"
        Write-Info "   Valitse 'Käynnistä' (1) asentaaksesi puuttuvat"
    }

    Write-Host ""
    Write-Host "Paina Enter palataksesi valikkoon..." -ForegroundColor Gray
    Read-Host
}

# Aja testit
function Run-Tests {
    Clear-Host
    Write-Header "═══════════════════════════════════════"
    Write-Header "  🧪 AJETAAN TESTIT"
    Write-Header "═══════════════════════════════════════"
    Write-Host ""

    $scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
    $projectDir = Split-Path -Parent $scriptDir
    & python "$projectDir\scripts\aja_testit.py"

    Write-Host ""
    Write-Host "Paina Enter palataksesi valikkoon..." -ForegroundColor Gray
    Read-Host
}

# Näytä ohjeet
function Show-Help {
    Clear-Host

    Draw-Box "📖 OHJEET" @(
        "",
        "1. Käynnistä uutislukija",
        "   → Asentaa automaattisesti puuttuvat osat",
        "   → Lukee tämän päivän uutiset",
        "   → Vahtii uusia uutisia",
        "",
        "2. Tarkista asennus",
        "   → Näyttää mitä on asennettu",
        "",
        "3. Aja testit",
        "   → Testaa että kaikki toimii",
        "",
        "PYSÄYTTÄMINEN:",
        "   Paina Ctrl+C lopettaaksesi uutisten lukemisen",
        "",
        "Projekti tehty rakkaudella ❤️"
    )

    Write-Host "Paina Enter palataksesi valikkoon..." -ForegroundColor Gray
    Read-Host
}

# Pääohjelma
function Main {
    # Jos action-parametri annettu, suorita se suoraan
    switch ($Action) {
        "start" { Start-Reader; return }
        "check" { Check-Installation; return }
        "test" { Run-Tests; return }
        "help" { Show-Help; return }
    }

    # Muuten näytä interaktiivinen valikko
    do {
        $choice = Show-Menu

        switch ($choice) {
            "1" { Start-Reader }
            "2" { Check-Installation }
            "3" { Run-Tests }
            "4" { Show-Help }
            "5" {
                Clear-Host
                Write-Host ""
                Write-Success "👋 Kiitos käytöstä!"
                Write-Host ""
                return
            }
            default {
                Write-Error "`n❌ Virheellinen valinta!"
                Start-Sleep -Seconds 1
            }
        }
    } while ($true)
}

# Käynnistä
try {
    Main
} catch {
    Write-Error "`n❌ Virhe: $_"
    Write-Host ""
    exit 1
}
