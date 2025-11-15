#!/usr/bin/env python3
"""
Nopea testi: Lue yksi uutinen cross-platform tavalla
"""

from uutistenlukija import NewsReader
import platform

print(f"Käyttöjärjestelmä: {platform.system()}")
print("-" * 50)

reader = NewsReader()

# Hae ja lue yksi uutinen
import feedparser

feed = feedparser.parse("https://feeds.yle.fi/uutiset/v1/recent.rss?publisherIds=YLE_UUTISET")

if feed.entries:
    entry = feed.entries[0]
    title = entry.get('title', 'Ei otsikkoa')

    print(f"Uutinen: {title}")
    print("Luetaan ääneen...\n")

    reader.speak_finnish(f"YLE Uutiset. {title}")

    print("✅ Valmis!")
else:
    print("❌ Ei uutisia saatavilla")
