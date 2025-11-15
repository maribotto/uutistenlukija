"""
Uutistenlukija - Konfiguraatio
"""

# RSS-feedit
RSS_FEEDS = [
    {
        "name": "Helsingin Sanomat",
        "url": "https://www.hs.fi/rss/tuoreimmat.xml"
    },
    {
        "name": "YLE Uutiset",
        "url": "https://feeds.yle.fi/uutiset/v1/recent.rss?publisherIds=YLE_UUTISET"
    }
]

# Asetukset
CHECK_INTERVAL = 300  # Tarkista 5 minuutin välein (sekunteina)

# Voit lisätä uusia RSS-feedejä lisäämällä tänne:
# RSS_FEEDS.append({
#     "name": "Uusi Lehti",
#     "url": "https://example.com/rss.xml"
# })
