#!/usr/bin/env python3
"""
Testi: Hae RSS-feed ja näytä uutisia
"""

import feedparser

RSS_FEED_URL = "https://www.hs.fi/rss/tuoreimmat.xml"

print(f"Haetaan feed: {RSS_FEED_URL}")
feed = feedparser.parse(RSS_FEED_URL)

if feed.bozo:
    print(f"Virhe: {feed.bozo_exception}")
else:
    print(f"\nLöytyi {len(feed.entries)} uutista")
    print("\nViimeiset 3 uutista:")
    for i, entry in enumerate(feed.entries[:3]):
        print(f"\n{i+1}. {entry.get('title', 'Ei otsikkoa')}")
        if 'summary' in entry:
            summary = entry.summary[:200]
            print(f"   {summary}...")
        print(f"   Link: {entry.get('link', 'Ei linkkiä')}")
