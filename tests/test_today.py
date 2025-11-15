#!/usr/bin/env python3
"""
Testaa tämän päivän uutisten hakua
"""

import feedparser
from datetime import datetime

RSS_FEEDS = [
    ("Helsingin Sanomat", "https://www.hs.fi/rss/tuoreimmat.xml"),
    ("YLE Uutiset", "https://feeds.yle.fi/uutiset/v1/recent.rss?publisherIds=YLE_UUTISET")
]

def is_today(entry):
    """Tarkista onko uutinen tältä päivältä"""
    try:
        if hasattr(entry, 'published_parsed') and entry.published_parsed:
            pub_time = datetime(*entry.published_parsed[:6])
        elif hasattr(entry, 'updated_parsed') and entry.updated_parsed:
            pub_time = datetime(*entry.updated_parsed[:6])
        else:
            return True

        today = datetime.now().date()
        return pub_time.date() == today
    except:
        return True

print("Haetaan tämän päivän uutiset...\n")
today_str = datetime.now().strftime('%Y-%m-%d')
print(f"Tänään: {today_str}\n")

for feed_name, feed_url in RSS_FEEDS:
    print(f"{'='*60}")
    print(f"Lähde: {feed_name}")
    print(f"{'='*60}")

    feed = feedparser.parse(feed_url)

    if feed.bozo:
        print(f"❌ Virhe: {feed.bozo_exception}\n")
        continue

    today_articles = []
    older_articles = []

    for entry in feed.entries:
        if is_today(entry):
            today_articles.append(entry)
        else:
            older_articles.append(entry)

    print(f"✓ Tänään: {len(today_articles)} uutista")
    print(f"  Vanhempia: {len(older_articles)} uutista")

    print(f"\nTämän päivän 5 ensimmäistä:")
    for i, entry in enumerate(today_articles[:5], 1):
        title = entry.get('title', 'Ei otsikkoa')

        # Hae aika
        time_str = "Ei aikaa"
        if hasattr(entry, 'published_parsed') and entry.published_parsed:
            pub_time = datetime(*entry.published_parsed[:6])
            time_str = pub_time.strftime('%H:%M')
        elif hasattr(entry, 'updated_parsed') and entry.updated_parsed:
            pub_time = datetime(*entry.updated_parsed[:6])
            time_str = pub_time.strftime('%H:%M')

        print(f"  {i}. [{time_str}] {title}")

    print("\n")

print("Valmis!")
