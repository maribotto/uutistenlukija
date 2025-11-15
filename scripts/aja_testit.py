#!/usr/bin/env python3
"""
Uutistenlukija - Automaattinen testien suoritus
Asentaa pytest:in ja ajaa kaikki testit
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

# Värikoodit
class Colors:
    GREEN = '\033[92m'
    BLUE = '\033[94m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    END = '\033[0m'

def print_header(text):
    """Tulosta otsikko"""
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{text:^60}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.END}\n")

def print_status(message, status="info"):
    """Tulosta statusviesti"""
    if status == "info":
        print(f"{Colors.BLUE}ℹ{Colors.END} {message}")
    elif status == "success":
        print(f"{Colors.GREEN}✓{Colors.END} {message}")
    elif status == "error":
        print(f"{Colors.RED}✗{Colors.END} {message}")
    elif status == "warning":
        print(f"{Colors.YELLOW}⚠{Colors.END} {message}")

BASE_DIR = Path(__file__).parent.resolve()
VENV_DIR = BASE_DIR / "venv"
SYSTEM = platform.system()

# Python-komennot
if SYSTEM == "Windows":
    PYTHON_CMD = str(VENV_DIR / "Scripts" / "python.exe")
    PIP_CMD = str(VENV_DIR / "Scripts" / "pip.exe")
    PYTEST_CMD = str(VENV_DIR / "Scripts" / "pytest.exe")
else:
    PYTHON_CMD = str(VENV_DIR / "bin" / "python3")
    PIP_CMD = str(VENV_DIR / "bin" / "pip3")
    PYTEST_CMD = str(VENV_DIR / "bin" / "pytest")

def check_venv():
    """Tarkista että virtuaaliympäristö on olemassa"""
    if not VENV_DIR.exists():
        print_status("Virtuaaliympäristöä ei löydy", "error")
        print_status("Aja ensin: python3 kaynnista.py --check-only", "info")
        sys.exit(1)
    print_status("Virtuaaliympäristö löytyi", "success")

def install_pytest():
    """Asenna pytest jos sitä ei ole"""
    print_status("Tarkistetaan pytest...")

    # Tarkista onko pytest asennettu
    try:
        result = subprocess.run(
            [PYTHON_CMD, "-c", "import pytest"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        if result.returncode == 0:
            print_status("pytest on asennettu", "success")
            return
    except:
        pass

    # Asenna pytest
    print_status("Asennetaan pytest...", "info")
    try:
        subprocess.run([PYTHON_CMD, "-m", "pip", "install", "-q", "pytest"], check=True)
        print_status("pytest asennettu", "success")
    except subprocess.CalledProcessError as e:
        print_status(f"Virhe pytest:in asennuksessa: {e}", "error")
        sys.exit(1)

def run_tests(args=None):
    """Aja testit"""
    print_header("AJETAAN TESTIT")

    # Rakenna pytest-komento
    cmd = [PYTEST_CMD, "-v"]

    # Lisää argumentit jos annettu
    if args:
        # Poista ensimmäinen argumentti (skriptin nimi)
        if args[0].endswith('aja_testit.py'):
            args = args[1:]
        cmd.extend(args)
    else:
        # Oletuksena: testaa kaikki paitsi hitaat testit
        cmd.extend(["-m", "not slow"])

    # Lisää tests-hakemisto
    cmd.append("tests/")

    print_status(f"Komento: {' '.join(cmd)}", "info")
    print()

    # Aja testit
    try:
        result = subprocess.run(cmd, cwd=BASE_DIR)
        return result.returncode
    except KeyboardInterrupt:
        print("\n")
        print_status("Testit keskeytetty", "warning")
        return 1
    except Exception as e:
        print_status(f"Virhe testien ajossa: {e}", "error")
        return 1

def main():
    """Pääohjelma"""
    print_header("UUTISTENLUKIJA - AUTOMAATTISET TESTIT")

    print_status(f"Käyttöjärjestelmä: {SYSTEM}", "info")
    print_status(f"Hakemisto: {BASE_DIR}", "info")
    print()

    # 1. Tarkista venv
    check_venv()

    # 2. Asenna pytest
    install_pytest()

    print()

    # 3. Aja testit
    exit_code = run_tests(sys.argv)

    print()
    if exit_code == 0:
        print_status("Kaikki testit menivät läpi!", "success")
    else:
        print_status("Jotkut testit epäonnistuivat", "error")

    sys.exit(exit_code)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n")
        print_status("Keskeytetty", "info")
        sys.exit(0)
    except Exception as e:
        print_status(f"Odottamaton virhe: {e}", "error")
        import traceback
        traceback.print_exc()
        sys.exit(1)
