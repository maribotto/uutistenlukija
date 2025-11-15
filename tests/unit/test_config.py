"""
Testit konfiguraatiolle
"""
import pytest

def test_config_imports():
    """Testaa että config-moduuli latautuu"""
    import config
    assert hasattr(config, 'RSS_FEEDS')
    assert hasattr(config, 'CHECK_INTERVAL')

def test_rss_feeds_structure():
    """Testaa RSS_FEEDS -listan rakenne"""
    import config

    assert isinstance(config.RSS_FEEDS, list)
    assert len(config.RSS_FEEDS) > 0

    for feed in config.RSS_FEEDS:
        assert isinstance(feed, dict)
        assert 'name' in feed
        assert 'url' in feed
        assert isinstance(feed['name'], str)
        assert isinstance(feed['url'], str)
        assert feed['url'].startswith('http')

def test_check_interval():
    """Testaa CHECK_INTERVAL arvo"""
    import config

    assert isinstance(config.CHECK_INTERVAL, int)
    assert config.CHECK_INTERVAL > 0
    assert config.CHECK_INTERVAL <= 3600  # Max 1 tunti

def test_helsingin_sanomat_feed():
    """Testaa että Helsingin Sanomat feed on mukana"""
    import config

    hs_feeds = [f for f in config.RSS_FEEDS if 'Helsingin Sanomat' in f['name']]
    assert len(hs_feeds) > 0

    hs_feed = hs_feeds[0]
    assert 'hs.fi' in hs_feed['url']

def test_yle_feed():
    """Testaa että YLE feed on mukana"""
    import config

    yle_feeds = [f for f in config.RSS_FEEDS if 'YLE' in f['name']]
    assert len(yle_feeds) > 0

    yle_feed = yle_feeds[0]
    assert 'yle.fi' in yle_feed['url']
