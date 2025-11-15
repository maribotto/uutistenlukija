#!/usr/bin/env python3
"""
Uutistenlukija - Helppokäyttöinen graafinen käynnistys
Isoäidin versio - Kaikki yhdellä klikkauksella!
"""

import sys
import os
import platform
import subprocess
from pathlib import Path

SYSTEM = platform.system()
BASE_DIR = Path(__file__).parent.resolve()

# Windows: Käytä PowerShell TUI:ta
if SYSTEM == "Windows":
    def main():
        print("🚀 Käynnistetään Windows TUI...")
        print()

        ps1_script = BASE_DIR / "kaynnista_tui.ps1"

        if not ps1_script.exists():
            print("❌ Virhe: kaynnista_tui.ps1 ei löytynyt!")
            print("Käytä sen sijaan: python kaynnista.py")
            sys.exit(1)

        try:
            # Käynnistä PowerShell TUI
            result = subprocess.run(
                ["powershell", "-ExecutionPolicy", "Bypass", "-File", str(ps1_script)],
                cwd=str(BASE_DIR)
            )
            sys.exit(result.returncode)
        except FileNotFoundError:
            print("❌ PowerShell ei löytynyt!")
            print("Käytä sen sijaan: python kaynnista.py")
            sys.exit(1)
        except Exception as e:
            print(f"❌ Virhe: {e}")
            print("Käytä sen sijaan: python kaynnista.py")
            sys.exit(1)

# Linux/macOS: Käytä curses TUI:ta (jos saatavilla)
else:
    # Tarkista curses
    try:
        import curses
        HAS_CURSES = True
    except ImportError:
        HAS_CURSES = False
        print("⚠️  Curses ei saatavilla - käytetään yksinkertaista tilaa")

    if HAS_CURSES:
        # Käytä TUI:ta
        from uutislukija_tui import UutislukijaTUI

        def main():
            print("🚀 Käynnistetään Uutistenlukija...")
            print("📺 Graafinen käyttöliittymä avautuu...")
            print()

            tui = UutislukijaTUI()
            tui.run()

            print("\n👋 Kiitos käytöstä!")
    else:
        # Yksinkertainen tekstitila
        def print_box(title, lines):
            """Tulosta laatikko"""
            width = max(len(line) for line in lines) + 4
            width = max(width, len(title) + 4)

            print("╔" + "═" * (width - 2) + "╗")
            print(f"║ {title:^{width-4}} ║")
            print("╠" + "═" * (width - 2) + "╣")

            for line in lines:
                padding = width - len(line) - 4
                print(f"║ {line}{' ' * padding} ║")

            print("╚" + "═" * (width - 2) + "╝")

        def simple_menu():
            """Yksinkertainen teksti-valikko"""
            while True:
                os.system('clear' if os.name != 'nt' else 'cls')

                print()
                print_box("🗞️  UUTISTENLUKIJA  🗞️", [
                    "Helsingin Sanomat & YLE",
                    "Suomeksi puhuen"
                ])
                print()

                menu = [
                    "",
                    "VALIKKO:",
                    "",
                    "1. 🚀 Käynnistä uutislukija",
                    "2. ⚙️  Tarkista asennus",
                    "3. 🧪 Aja testit",
                    "4. 📖 Näytä ohjeet",
                    "5. 🚪 Lopeta",
                    ""
                ]

                for line in menu:
                    if line:
                        print(f"  {line}")
                    else:
                        print()

                choice = input("\nValitse (1-5): ").strip()

                if choice == "1":
                    os.system(f"{sys.executable} kaynnista.py")
                elif choice == "2":
                    os.system(f"{sys.executable} scripts/tarkista_asennus.py")
                    input("\nPaina Enter jatkaaksesi...")
                elif choice == "3":
                    os.system(f"{sys.executable} scripts/aja_testit.py")
                    input("\nPaina Enter jatkaaksesi...")
                elif choice == "4":
                    show_help()
                    input("\nPaina Enter jatkaaksesi...")
                elif choice == "5":
                    print("\n👋 Kiitos käytöstä!\n")
                    break
                else:
                    print("\n❌ Virheellinen valinta!")
                    input("Paina Enter jatkaaksesi...")

        def show_help():
            """Näytä ohjeet"""
            print()
            print_box("OHJEET", [
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
                "Projekti tehty rakkaudella ❤️"
            ])

        def main():
            """Pääohjelma yksinkertaisessa tilassa"""
            simple_menu()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Näkemiin!\n")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Virhe: {e}\n")
        sys.exit(1)
