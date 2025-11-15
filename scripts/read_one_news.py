#!/usr/bin/env python3
"""
Lue yksi kokonainen uutinen RSS-feedistä
"""

import feedparser
import subprocess
import html
import re

RSS_FEED_URL = "https://www.hs.fi/rss/tuoreimmat.xml"
PIPER_PATH = "/home/kaanders/hesari-puhe/piper/piper"
PIPER_MODEL = "/home/kaanders/hesari-puhe/fi_FI-asmo-medium.onnx"

def clean_html(text):
    """Poista HTML-tagit ja puhdista teksti"""
    # Poista HTML-tagit
    text = re.sub(r'<[^>]+>', '', text)
    # Dekoodaa HTML-entiteetit
    text = html.unescape(text)
    # Poista ylimääräiset välilyönnit ja rivinvaihdot
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def speak_finnish(text):
    """Lausu teksti suomeksi Piperillä"""
    try:
        clean_text = text.replace('\n', ' ').strip()

        echo = subprocess.Popen(
            ['echo', clean_text],
            stdout=subprocess.PIPE
        )

        piper = subprocess.Popen(
            [PIPER_PATH, '--model', PIPER_MODEL, '--output_file', '-'],
            stdin=echo.stdout,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL
        )

        aplay = subprocess.Popen(
            ['aplay', '-q'],
            stdin=piper.stdout,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

        echo.stdout.close()
        piper.stdout.close()
        aplay.wait()

    except Exception as e:
        print(f"Virhe puhesynteesissa: {e}")

print("Haetaan uusin uutinen...")
feed = feedparser.parse(RSS_FEED_URL)

if not feed.bozo and len(feed.entries) > 0:
    entry = feed.entries[0]

    title = entry.get('title', 'Ei otsikkoa')
    summary = entry.get('summary', '')
    link = entry.get('link', '')

    # Puhdista tiivistelmä HTML-tageista
    summary_clean = clean_html(summary)

    print(f"\n{'='*60}")
    print(f"Uutinen: {title}")
    print(f"{'='*60}\n")
    print(f"Tiivistelmä: {summary_clean[:200]}...")
    print(f"\nLinkki: {link}\n")
    print("Luetaan ääneen...\n")

    # Lue otsikko
    speak_finnish(f"Uutinen. {title}.")

    # Pieni tauko
    import time
    time.sleep(0.5)

    # Lue tiivistelmä
    if summary_clean:
        speak_finnish(summary_clean)

    print("\nValmis!")
else:
    print("Ei uutisia saatavilla")
