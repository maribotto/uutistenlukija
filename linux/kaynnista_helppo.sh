#!/bin/bash
# Uutistenlukija - Linux käynnistin
# Tuplaklikkaus terminaalissa

# Siirry projektijuureen (yksi taso ylöspäin skriptin hakemistosta)
cd "$(dirname "$0")/.." || exit 1

# Tyhjennä näyttö ja näytä otsikko
clear
echo ""
echo "╔══════════════════════════════════════╗"
echo "║   🗞️  UUTISTENLUKIJA - LINUX  🗞️    ║"
echo "╚══════════════════════════════════════╝"
echo ""
echo "Käynnistetään..."
echo ""

# Tarkista onko Python3 asennettu
if ! command -v python3 &> /dev/null; then
    echo "❌ Virhe: Python 3 ei ole asennettu!"
    echo ""
    echo "Asenna Python:"
    echo "  Ubuntu/Debian: sudo apt install python3 python3-venv"
    echo "  Fedora: sudo dnf install python3"
    echo "  Arch: sudo pacman -S python"
    echo ""
    read -p "Paina Enter sulkeaksesi..."
    exit 1
fi

# Käynnistä TUI
python3 kaynnista_helppo.py

# Pidä ikkuna auki jos ohjelma kaatui
EXIT_CODE=$?
if [ $EXIT_CODE -ne 0 ]; then
    echo ""
    echo "⚠️  Ohjelma päättyi virheeseen (koodi: $EXIT_CODE)."
    echo ""
    read -p "Paina Enter sulkeaksesi..."
fi
