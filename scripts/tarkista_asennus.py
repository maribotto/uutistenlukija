#!/usr/bin/env python3
"""
Tarkista että kaikki komponentit on asennettu
"""

import sys
from pathlib import Path

BASE_DIR = Path(__file__).parent.resolve()

checks = [
    ("Virtuaaliympäristö", BASE_DIR / "venv"),
    ("Piper TTS (piper-hakemisto)", BASE_DIR / "piper"),
    ("Äänimalli (.onnx)", BASE_DIR / "fi_FI-asmo-medium.onnx"),
    ("Mallin config (.json)", BASE_DIR / "fi_FI-asmo-medium.onnx.json"),
    ("Pääohjelma", BASE_DIR / "uutistenlukija.py"),
    ("Konfiguraatio", BASE_DIR / "config.py"),
]

print("🔍 Tarkistetaan asennus...\n")

all_ok = True
for name, path in checks:
    if path.exists():
        print(f"✓ {name}")
    else:
        print(f"✗ {name} - PUUTTUU!")
        all_ok = False

if all_ok:
    print("\n✅ Kaikki komponentit asennettu!")
    print("\nVoit käynnistää ohjelman:")
    print("  python3 kaynnista.py")
else:
    print("\n⚠️  Joitain komponentteja puuttuu")
    print("\nSuorita asennus:")
    print("  python3 kaynnista.py")
    sys.exit(1)
