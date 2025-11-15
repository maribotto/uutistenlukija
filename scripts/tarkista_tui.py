#!/usr/bin/env python3
"""
Tarkista TUI-integraatio ilman TTY:tä
"""

import sys
from pathlib import Path

def main():
    BASE_DIR = Path(__file__).parent.resolve()

    print("🔍 Tarkistetaan TUI-integraatio...\n")

    checks_passed = 0
    checks_total = 0

    # 1. Tarkista että tiedostot ovat olemassa
    files_to_check = [
        "uutislukija_tui.py",
        "kaynnista_helppo.py",
        "kaynnista.py",
        "aja_testit.py",
        "tarkista_asennus.py"
    ]

    for filename in files_to_check:
        checks_total += 1
        filepath = BASE_DIR / filename
        if filepath.exists():
            print(f"✓ {filename} löytyy")
            checks_passed += 1
        else:
            print(f"✗ {filename} puuttuu!")

    print()

    # 2. Tarkista että moduulit importataan
    modules_to_import = [
        "uutislukija_tui",
        "kaynnista_helppo"
    ]

    for module_name in modules_to_import:
        checks_total += 1
        try:
            __import__(module_name)
            print(f"✓ {module_name} importataan onnistuneesti")
            checks_passed += 1
        except ImportError as e:
            print(f"✗ {module_name} ei importata: {e}")

    print()

    # 3. Tarkista TUI-luokan rakenne
    checks_total += 1
    try:
        from uutislukija_tui import UutislukijaTUI
        tui = UutislukijaTUI()

        # Tarkista että metodit ovat olemassa
        required_methods = [
            "start_reader",
            "check_installation",
            "run_tests",
            "show_help",
            "main_loop",
            "run"
        ]

        all_methods_exist = True
        for method_name in required_methods:
            if not hasattr(tui, method_name):
                print(f"✗ Metodi {method_name} puuttuu!")
                all_methods_exist = False

        if all_methods_exist:
            print("✓ TUI-luokalla on kaikki tarvittavat metodit")
            checks_passed += 1

    except Exception as e:
        print(f"✗ TUI-luokan tarkistus epäonnistui: {e}")

    print()

    # 4. Tarkista että kaynnista_helppo.py:llä on curses-fallback
    checks_total += 1
    try:
        with open(BASE_DIR / "kaynnista_helppo.py", "r", encoding="utf-8") as f:
            content = f.read()
            if "HAS_CURSES" in content and "simple_menu" in content:
                print("✓ kaynnista_helppo.py:llä on curses-fallback")
                checks_passed += 1
            else:
                print("✗ kaynnista_helppo.py:ltä puuttuu curses-fallback")
    except Exception as e:
        print(f"✗ kaynnista_helppo.py:n tarkistus epäonnistui: {e}")

    print()

    # 5. Yhteenveto
    print("=" * 50)
    print(f"Tarkistuksia suoritettu: {checks_total}")
    print(f"Onnistui: {checks_passed}")
    print(f"Epäonnistui: {checks_total - checks_passed}")
    print("=" * 50)

    if checks_passed == checks_total:
        print("\n✅ KAIKKI TARKISTUKSET LÄPI!")
        print("\nTUI-integraatio on valmis käyttöön.")
        print("\nKäynnistä TUI:")
        print("  python3 kaynnista_helppo.py")
        print("\nHuom: TUI vaatii oikean terminaalin toimiakseen.")
        print("Jos curses ei toimi, käytetään yksinkertaista teksti-valikkoa.")
        return 0
    else:
        print("\n⚠️  JOITAIN TARKISTUKSIA EI LÄPÄISTY")
        return 1

if __name__ == "__main__":
    sys.exit(main())
