#!/bin/bash
# Uutislukija - Käynnistysskripti Linux/macOS

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR/.."

echo "Uutislukija (HS & YLE)"
echo "======================"
echo ""

# Tarkista että virtuaaliympäristö on olemassa
if [ ! -f "venv/bin/python3" ]; then
    echo "VIRHE: Python virtuaaliympäristö ei löydy!"
    echo "Aja ensin: python3 -m venv venv"
    echo ""
    exit 1
fi

# Käynnistä ohjelma
./venv/bin/python3 uutistenlukija.py
