"""
Integraatiotestit RSS-fedeille
"""
import pytest
import feedparser
import config

@pytest.mark.slow
def test_helsingin_sanomat_feed_accessible():
    """Testaa että HS RSS-feed on saavutettavissa"""
    hs_feeds = [f for f in config.RSS_FEEDS if 'Helsingin Sanomat' in f['name']]
    assert len(hs_feeds) > 0

    feed_url = hs_feeds[0]['url']
    feed = feedparser.parse(feed_url)

    # Tarkista että feed ei ole tyhjä
    assert not feed.bozo or len(feed.entries) > 0
    assert len(feed.entries) > 0

    # Tarkista että entries sisältää tarvittavat kentät
    first_entry = feed.entries[0]
    assert hasattr(first_entry, 'title') or 'title' in first_entry
    assert hasattr(first_entry, 'link') or 'link' in first_entry

@pytest.mark.slow
def test_yle_feed_accessible():
    """Testaa että YLE RSS-feed on saavutettavissa"""
    yle_feeds = [f for f in config.RSS_FEEDS if 'YLE' in f['name']]
    assert len(yle_feeds) > 0

    feed_url = yle_feeds[0]['url']
    feed = feedparser.parse(feed_url)

    # Tarkista että feed ei ole tyhjä
    assert not feed.bozo or len(feed.entries) > 0
    assert len(feed.entries) > 0

    # Tarkista että entries sisältää tarvittavat kentät
    first_entry = feed.entries[0]
    assert hasattr(first_entry, 'title') or 'title' in first_entry
    assert hasattr(first_entry, 'link') or 'link' in first_entry

@pytest.mark.slow
def test_all_feeds_valid():
    """Testaa että kaikki RSS-feedit ovat valideja"""
    for feed_info in config.RSS_FEEDS:
        feed = feedparser.parse(feed_info['url'])

        # Feed ei saa olla täysin rikki
        assert not feed.bozo or len(feed.entries) > 0

        # Pitää olla vähintään yksi entry
        assert len(feed.entries) > 0, f"Feed {feed_info['name']} on tyhjä"

def test_mock_rss_feed_parsing(mock_rss_feed):
    """Testaa RSS-feedin parsimista mock datalla"""
    feed = feedparser.parse(mock_rss_feed)

    assert len(feed.entries) == 2
    assert feed.entries[0].title == "Testiotsikko 1"
    assert feed.entries[1].title == "Testiotsikko 2"
