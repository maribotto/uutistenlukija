#!/bin/bash
# Uutistenlukija - macOS käynnistin
# Tuplaklikkaus Terminal.app:ssa

# Siirry projektijuureen (yksi taso ylöspäin skriptin hakemistosta)
cd "$(dirname "$0")/.." || exit 1

# Tyhjennä näyttö ja näytä otsikko
clear
echo ""
echo "╔══════════════════════════════════════╗"
echo "║   🗞️  UUTISTENLUKIJA - macOS  🗞️    ║"
echo "╚══════════════════════════════════════╝"
echo ""
echo "Käynnistetään..."
echo ""

# Tarkista onko Python3 asennettu
if ! command -v python3 &> /dev/null; then
    echo "❌ Virhe: Python 3 ei ole asennettu!"
    echo ""
    echo "Asenna Python:"
    echo "  brew install python@3.11"
    echo ""
    echo "TAI lataa: https://www.python.org/downloads/"
    echo ""
    read -p "Paina Enter sulkeaksesi..."
    exit 1
fi

# Käynnistä TUI
python3 kaynnista_helppo.py

# Pidä ikkuna auki jos ohjelma kaatui
if [ $? -ne 0 ]; then
    echo ""
    echo "⚠️  Ohjelma päättyi virheeseen."
    echo ""
    read -p "Paina Enter sulkeaksesi..."
fi
