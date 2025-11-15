#!/usr/bin/env python3
"""
Testi: Lue yksi uutinen ääneen Piperillä (HS & YLE)
"""

import feedparser
import subprocess

RSS_FEEDS = [
    ("Helsingin Sanomat", "https://www.hs.fi/rss/tuoreimmat.xml"),
    ("YLE Uutiset", "https://feeds.yle.fi/uutiset/v1/recent.rss?publisherIds=YLE_UUTISET")
]
PIPER_PATH = "/home/kaanders/hesari-puhe/piper/piper"
PIPER_MODEL = "/home/kaanders/hesari-puhe/fi_FI-asmo-medium.onnx"

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

        print("✓ Lausuttu Piperillä")
    except Exception as e:
        print(f"✗ Virhe: {e}")

print("Haetaan uusimmat uutiset...\n")

for feed_name, feed_url in RSS_FEEDS:
    print(f"Lähde: {feed_name}")
    feed = feedparser.parse(feed_url)

    if not feed.bozo and len(feed.entries) > 0:
        entry = feed.entries[0]
        title = entry.get('title', 'Ei otsikkoa')

        print(f"  Uutinen: {title}")
        print(f"  Luetaan ääneen...")
        speak_finnish(f"{feed_name}. {title}")
        print()
    else:
        print(f"  Ei uutisia saatavilla\n")

print("Valmis!")
