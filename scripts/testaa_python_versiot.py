#!/usr/bin/env python3
"""
Testaa uutistenlukija-projekti eri Python-versioilla
"""

import subprocess
import sys
import json
from pathlib import Path
from datetime import datetime

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
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*70}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{text:^70}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*70}{Colors.END}\n")

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

# Python-versiot jotka testataan
PYTHON_VERSIONS = [
    "python3.10",
    "python3.11",
    "python3.12",
]

def check_python_available(python_cmd):
    """Tarkista onko Python-versio saatavilla"""
    try:
        result = subprocess.run(
            [python_cmd, "--version"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            version = result.stdout.strip()
            return True, version
        return False, None
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False, None

def test_python_version(python_cmd):
    """Testaa projektia tietyllä Python-versiolla"""
    available, version = check_python_available(python_cmd)

    if not available:
        return {
            "python": python_cmd,
            "available": False,
            "version": None,
            "tests": {}
        }

    print_status(f"Testataan: {version}", "info")

    results = {
        "python": python_cmd,
        "available": True,
        "version": version,
        "tests": {}
    }

    # Testi 1: Venv-luonti
    print("  └─ Luodaan virtuaaliympäristö...", end=" ", flush=True)
    venv_dir = BASE_DIR / f".test_venv_{python_cmd.replace('python', 'py')}"

    try:
        # Poista vanha venv jos on
        if venv_dir.exists():
            subprocess.run(["rm", "-rf", str(venv_dir)], check=True)

        result = subprocess.run(
            [python_cmd, "-m", "venv", str(venv_dir)],
            capture_output=True,
            text=True,
            timeout=30
        )
        if result.returncode == 0:
            print(f"{Colors.GREEN}✓{Colors.END}")
            results["tests"]["venv_creation"] = True
        else:
            # Yritä ilman pip:iä jos ensurepip epäonnistuu
            result2 = subprocess.run(
                [python_cmd, "-m", "venv", "--without-pip", str(venv_dir)],
                capture_output=True,
                text=True,
                timeout=30
            )
            if result2.returncode == 0:
                print(f"{Colors.YELLOW}⚠{Colors.END} (ilman pip)")
                results["tests"]["venv_creation"] = True
                results["tests"]["venv_without_pip"] = True
            else:
                print(f"{Colors.RED}✗{Colors.END}")
                results["tests"]["venv_creation"] = False
                results["tests"]["venv_error"] = result.stderr or result2.stderr
                return results
    except Exception as e:
        print(f"{Colors.RED}✗{Colors.END} ({e})")
        results["tests"]["venv_creation"] = False
        return results

    # Testi 2: Riippuvuuksien asennus
    print("  └─ Asennetaan riippuvuudet...", end=" ", flush=True)
    python_venv = str(venv_dir / "bin" / "python3")

    try:
        result = subprocess.run(
            [python_venv, "-m", "pip", "install", "-q", "feedparser"],
            capture_output=True,
            timeout=60
        )
        if result.returncode == 0:
            print(f"{Colors.GREEN}✓{Colors.END}")
            results["tests"]["install_deps"] = True
        else:
            print(f"{Colors.RED}✗{Colors.END}")
            results["tests"]["install_deps"] = False
            return results
    except Exception as e:
        print(f"{Colors.RED}✗{Colors.END} ({e})")
        results["tests"]["install_deps"] = False
        return results

    # Testi 3: Import-testit
    print("  └─ Testataan importit...", end=" ", flush=True)

    try:
        # Testaa että moduulit latautuvat
        test_script = """
import sys
sys.path.insert(0, '.')
import config
import uutistenlukija
print('OK')
"""
        result = subprocess.run(
            [python_venv, "-c", test_script],
            capture_output=True,
            text=True,
            cwd=BASE_DIR,
            timeout=10
        )
        if result.returncode == 0 and "OK" in result.stdout:
            print(f"{Colors.GREEN}✓{Colors.END}")
            results["tests"]["imports"] = True
        else:
            print(f"{Colors.RED}✗{Colors.END}")
            results["tests"]["imports"] = False
            return results
    except Exception as e:
        print(f"{Colors.RED}✗{Colors.END} ({e})")
        results["tests"]["imports"] = False
        return results

    # Testi 4: Yksikkötestit (jos pytest on saatavilla)
    print("  └─ Ajetaan testit...", end=" ", flush=True)

    try:
        # Asenna pytest
        subprocess.run(
            [python_venv, "-m", "pip", "install", "-q", "pytest"],
            capture_output=True,
            timeout=60
        )

        pytest_cmd = str(venv_dir / "bin" / "pytest")
        result = subprocess.run(
            [pytest_cmd, "-q", "--tb=no", "-m", "not slow", "tests/"],
            capture_output=True,
            text=True,
            cwd=BASE_DIR,
            timeout=60
        )

        # Parsii tulokset
        if "passed" in result.stdout:
            print(f"{Colors.GREEN}✓{Colors.END}")
            results["tests"]["pytest"] = True
            # Yritä parseta testien määrä
            import re
            match = re.search(r'(\d+) passed', result.stdout)
            if match:
                results["tests"]["pytest_count"] = int(match.group(1))
        else:
            print(f"{Colors.RED}✗{Colors.END}")
            results["tests"]["pytest"] = False
    except Exception as e:
        print(f"{Colors.YELLOW}⚠{Colors.END} (skipped: {e})")
        results["tests"]["pytest"] = None

    # Siivoa
    try:
        subprocess.run(["rm", "-rf", str(venv_dir)], check=True)
    except:
        pass

    return results

def main():
    """Pääohjelma"""
    print_header("PYTHON-VERSIOIDEN YHTEENSOPIVUUSTESTIT")

    print_status(f"Testataan {len(PYTHON_VERSIONS)} Python-versiota", "info")
    print_status(f"Projekti: {BASE_DIR}", "info")
    print()

    all_results = []

    for python_cmd in PYTHON_VERSIONS:
        print(f"\n{Colors.BOLD}Testing {python_cmd}:{Colors.END}")
        results = test_python_version(python_cmd)
        all_results.append(results)

    # Yhteenveto
    print_header("YHTEENVETO")

    compatible_versions = []

    for result in all_results:
        if not result["available"]:
            print(f"{Colors.YELLOW}⚠{Colors.END} {result['python']:15} - Ei saatavilla")
            continue

        # Tarkista että pakolliset testit (ei pytest) ovat läpäisseet
        required_tests = ["venv_creation", "install_deps", "imports"]
        all_passed = all(
            result["tests"].get(test) == True for test in required_tests
        )

        if all_passed:
            status = f"{Colors.GREEN}✓ TOIMII{Colors.END}"
            compatible_versions.append(result["version"])
        else:
            status = f"{Colors.RED}✗ EI TOIMI{Colors.END}"

        pytest_info = ""
        if result["tests"].get("pytest") == True:
            count = result["tests"].get("pytest_count", "?")
            pytest_info = f" ({count} testiä)"

        print(f"{status:30} {result['version']}{pytest_info}")

    print()
    print_status(f"Yhteensopivat versiot: {len(compatible_versions)}/{len([r for r in all_results if r['available']])}", "success")

    # Tallenna tulokset
    output_file = BASE_DIR / "PYTHON_COMPATIBILITY.json"
    with open(output_file, 'w') as f:
        json.dump({
            "tested_at": datetime.now().isoformat(),
            "results": all_results,
            "compatible_versions": compatible_versions
        }, f, indent=2)

    print_status(f"Tulokset tallennettu: {output_file}", "info")

    return 0 if len(compatible_versions) > 0 else 1

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n")
        print_status("Keskeytetty", "info")
        sys.exit(1)
