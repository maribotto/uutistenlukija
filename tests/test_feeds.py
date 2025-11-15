#!/usr/bin/env python3
"""
Testaa RSS-feedit ilman puhesynteesiä
"""

import feedparser

RSS_FEEDS = [
    ("Helsingin Sanomat", "https://www.hs.fi/rss/tuoreimmat.xml"),
    ("YLE Uutiset", "https://feeds.yle.fi/uutiset/v1/recent.rss?publisherIds=YLE_UUTISET")
]

print("Testataan RSS-feedit...\n")

for feed_name, feed_url in RSS_FEEDS:
    print(f"{'='*60}")
    print(f"Lähde: {feed_name}")
    print(f"{'='*60}")

    feed = feedparser.parse(feed_url)

    if feed.bozo:
        print(f"❌ Virhe: {feed.bozo_exception}\n")
        continue

    print(f"✓ Löytyi {len(feed.entries)} uutista\n")

    print("Viimeiset 3 uutista:")
    for i, entry in enumerate(feed.entries[:3], 1):
        title = entry.get('title', 'Ei otsikkoa')
        link = entry.get('link', 'Ei linkkiä')
        print(f"\n{i}. {title}")
        print(f"   {link}")

    print("\n")

print("Valmis!")
