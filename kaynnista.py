#!/usr/bin/env python3
"""
Uutistenlukija - Universaali käynnistys- ja asennusohjelma
Toimii Windowsissa, macOS:ssa ja Linuxissa
Asentaa automaattisesti kaikki tarvittavat komponentit ensimmäisellä kerralla
"""

import os
import sys
import platform
import subprocess
import urllib.request
import tarfile
import zipfile
from pathlib import Path

# Värikoodit terminaalille
class Colors:
    GREEN = '\033[92m'
    BLUE = '\033[94m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    END = '\033[0m'

def print_status(message, status="info"):
    """Tulosta värillinen statusviesti"""
    if status == "info":
        print(f"{Colors.BLUE}ℹ{Colors.END} {message}")
    elif status == "success":
        print(f"{Colors.GREEN}✓{Colors.END} {message}")
    elif status == "error":
        print(f"{Colors.RED}✗{Colors.END} {message}")
    elif status == "warning":
        print(f"{Colors.YELLOW}⚠{Colors.END} {message}")

def print_header(text):
    """Tulosta otsikko"""
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{text:^60}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.END}\n")

# Tunnista käyttöjärjestelmä
SYSTEM = platform.system()
BASE_DIR = Path(__file__).parent.resolve()
VENV_DIR = BASE_DIR / "venv"
PIPER_DIR = BASE_DIR / "piper"
VOICE_MODEL = BASE_DIR / "fi_FI-asmo-medium.onnx"
VOICE_CONFIG = BASE_DIR / "fi_FI-asmo-medium.onnx.json"

# Määritä Python-komennot käyttöjärjestelmän mukaan
if SYSTEM == "Windows":
    PYTHON_CMD = str(VENV_DIR / "Scripts" / "python.exe")
    PIP_CMD = str(VENV_DIR / "Scripts" / "pip.exe")
    PIPER_URL = "https://github.com/rhasspy/piper/releases/download/v1.2.0/piper_windows_amd64.zip"
    PIPER_EXECUTABLE = PIPER_DIR / "piper.exe"
else:
    PYTHON_CMD = str(VENV_DIR / "bin" / "python3")
    PIP_CMD = str(VENV_DIR / "bin" / "pip")
    if SYSTEM == "Darwin":  # macOS
        # Tarkista arkkitehtuuri (ARM64 vs x86_64)
        arch = platform.machine()
        if arch == "arm64":
            PIPER_URL = "https://github.com/rhasspy/piper/releases/download/v1.2.0/piper_macos_arm64.tar.gz"
        else:
            PIPER_URL = "https://github.com/rhasspy/piper/releases/download/v1.2.0/piper_macos_x64.tar.gz"
    else:  # Linux
        PIPER_URL = "https://github.com/rhasspy/piper/releases/download/v1.2.0/piper_linux_x86_64.tar.gz"
    PIPER_EXECUTABLE = PIPER_DIR / "piper"

# Äänimallin URL
VOICE_MODEL_URL = "https://huggingface.co/AsmoKoskinen/Piper_Finnish_Model/resolve/main/fi_FI-asmo-medium.onnx"
VOICE_CONFIG_URL = "https://huggingface.co/AsmoKoskinen/Piper_Finnish_Model/resolve/main/fi_FI-asmo-medium.onnx.json"

def check_python_version():
    """Tarkista että Python-versio on riittävän uusi"""
    print_status("Tarkistetaan Python-versio...")
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 7):
        print_status(f"Python 3.7+ vaaditaan. Sinulla on Python {version.major}.{version.minor}", "error")
        sys.exit(1)
    print_status(f"Python {version.major}.{version.minor}.{version.micro} OK", "success")

def create_venv():
    """Luo virtuaaliympäristö jos sitä ei ole"""
    if VENV_DIR.exists():
        print_status("Virtuaaliympäristö löytyy", "success")
        return

    print_status("Luodaan virtuaaliympäristö...")
    try:
        subprocess.run([sys.executable, "-m", "venv", str(VENV_DIR)], check=True)
        print_status("Virtuaaliympäristö luotu", "success")
    except subprocess.CalledProcessError as e:
        print_status(f"Virhe virtuaaliympäristön luomisessa: {e}", "error")
        sys.exit(1)

def install_dependencies():
    """Asenna Python-riippuvuudet"""
    print_status("Tarkistetaan Python-riippuvuudet...")

    # Tarkista onko feedparser asennettu
    try:
        result = subprocess.run(
            [PYTHON_CMD, "-c", "import feedparser"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        if result.returncode == 0:
            print_status("Riippuvuudet asennettu", "success")
            return
    except:
        pass

    print_status("Asennetaan feedparser...")
    try:
        subprocess.run([PIP_CMD, "install", "-q", "feedparser"], check=True)
        print_status("Riippuvuudet asennettu", "success")
    except subprocess.CalledProcessError as e:
        print_status(f"Virhe riippuvuuksien asennuksessa: {e}", "error")
        sys.exit(1)

def download_file(url, destination, description):
    """Lataa tiedosto näyttäen edistymisen"""
    print_status(f"Ladataan {description}...")

    def show_progress(block_num, block_size, total_size):
        downloaded = block_num * block_size
        percent = min(100, downloaded * 100 / total_size)
        bar_length = 40
        filled = int(bar_length * percent / 100)
        bar = '█' * filled + '░' * (bar_length - filled)
        print(f"\r  [{bar}] {percent:.1f}% ", end='', flush=True)

    try:
        urllib.request.urlretrieve(url, destination, show_progress)
        print()  # Uusi rivi progressbarin jälkeen
        print_status(f"{description} ladattu", "success")
    except Exception as e:
        print()
        print_status(f"Virhe latauksessa: {e}", "error")
        sys.exit(1)

def install_piper():
    """Lataa ja asenna Piper TTS"""
    if PIPER_EXECUTABLE.exists():
        print_status("Piper TTS löytyy", "success")
        return

    print_status(f"Asennetaan Piper TTS ({SYSTEM})...")

    # Luo piper-hakemisto
    PIPER_DIR.mkdir(exist_ok=True)

    # Lataa Piper
    archive_name = "piper_archive.zip" if SYSTEM == "Windows" else "piper_archive.tar.gz"
    archive_path = BASE_DIR / archive_name

    download_file(PIPER_URL, archive_path, "Piper TTS")

    # Pura arkisto
    print_status("Puretaan arkistoa...")
    try:
        if SYSTEM == "Windows":
            with zipfile.ZipFile(archive_path, 'r') as zip_ref:
                zip_ref.extractall(BASE_DIR)
        else:
            with tarfile.open(archive_path, 'r:gz') as tar_ref:
                tar_ref.extractall(BASE_DIR)

        # Poista arkisto
        archive_path.unlink()

        # Tee Piper suoritettavaksi (Unix)
        if SYSTEM != "Windows":
            PIPER_EXECUTABLE.chmod(0o755)

        print_status("Piper TTS asennettu", "success")
    except Exception as e:
        print_status(f"Virhe arkiston purkamisessa: {e}", "error")
        sys.exit(1)

def install_voice_model():
    """Lataa suomenkielinen äänimalli"""
    if VOICE_MODEL.exists() and VOICE_CONFIG.exists():
        print_status("Äänimalli löytyy", "success")
        return

    print_status("Asennetaan suomenkielinen äänimalli...")

    # Lataa malli
    if not VOICE_MODEL.exists():
        download_file(VOICE_MODEL_URL, VOICE_MODEL, "äänimalli (.onnx)")

    # Lataa konfiguraatio
    if not VOICE_CONFIG.exists():
        download_file(VOICE_CONFIG_URL, VOICE_CONFIG, "mallin konfiguraatio (.json)")

    print_status("Äänimalli asennettu", "success")

def run_application():
    """Käynnistä uutistenlukija"""
    print_header("KÄYNNISTETÄÄN UUTISTENLUKIJA")

    main_script = BASE_DIR / "uutistenlukija.py"
    if not main_script.exists():
        print_status("Virhe: uutistenlukija.py ei löydy!", "error")
        sys.exit(1)

    try:
        subprocess.run([PYTHON_CMD, str(main_script)])
    except KeyboardInterrupt:
        print("\n")
        print_status("Lopetettu käyttäjän pyynnöstä", "info")
    except Exception as e:
        print_status(f"Virhe ohjelman suorituksessa: {e}", "error")
        sys.exit(1)

def main():
    """Pääohjelma"""
    # Tarkista onko --check-only parametri
    check_only = "--check-only" in sys.argv

    print_header("UUTISTENLUKIJA - AUTOMAATTINEN ASENNUS")

    print_status(f"Käyttöjärjestelmä: {SYSTEM}", "info")
    print_status(f"Hakemisto: {BASE_DIR}", "info")
    print()

    # 1. Tarkista Python-versio
    check_python_version()

    # 2. Luo virtuaaliympäristö
    create_venv()

    # 3. Asenna riippuvuudet
    install_dependencies()

    # 4. Asenna Piper TTS
    install_piper()

    # 5. Asenna äänimalli
    install_voice_model()

    print()
    print_status("Kaikki komponentit asennettu!", "success")
    print()

    # 6. Käynnistä ohjelma (jos ei ole --check-only)
    if check_only:
        print_status("Asennuksen tarkistus valmis. Käynnistä ohjelma: python3 kaynnista.py", "info")
    else:
        run_application()

if __name__ == "__main__":
    # Tarkista onko interaktiivinen sessio (tuplaklikkaus Windowsissa)
    is_interactive = sys.stdin.isatty() and SYSTEM == "Windows"

    try:
        main()

        # Jos Windows ja interaktiivinen, pidä ikkuna auki
        if is_interactive:
            print("\n" + "="*60)
            print("Uutislukija on nyt käynnissä!")
            print("Pysäytä painamalla Ctrl+C")
            print("="*60)
            try:
                # Pidä ikkuna auki
                while True:
                    import time
                    time.sleep(1)
            except KeyboardInterrupt:
                print_status("\nPysäytetty käyttäjän toimesta", "info")

    except KeyboardInterrupt:
        print("\n")
        print_status("Keskeytetty", "info")
        if is_interactive:
            input("\nPaina Enter sulkeaksesi...")
        sys.exit(0)
    except Exception as e:
        print_status(f"Odottamaton virhe: {e}", "error")
        import traceback
        traceback.print_exc()
        if is_interactive:
            input("\nPaina Enter sulkeaksesi...")
        sys.exit(1)
