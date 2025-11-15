"""
Pytest configuration and fixtures
"""
import sys
import pytest
from pathlib import Path

# Lisää projektin juurihakemisto Pythonin polkuun
BASE_DIR = Path(__file__).parent.parent.resolve()
sys.path.insert(0, str(BASE_DIR))

@pytest.fixture
def base_dir():
    """Projektin juurihakemisto"""
    return BASE_DIR

@pytest.fixture
def test_data_dir():
    """Testidatan hakemisto"""
    test_dir = Path(__file__).parent / "test_data"
    test_dir.mkdir(exist_ok=True)
    return test_dir

@pytest.fixture
def mock_rss_feed():
    """Mock RSS feed data"""
    return """<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
    <channel>
        <title>Test News</title>
        <item>
            <title>Testiotsikko 1</title>
            <link>https://example.com/1</link>
            <description>Testi kuvaus 1</description>
            <pubDate>Fri, 15 Nov 2024 12:00:00 GMT</pubDate>
        </item>
        <item>
            <title>Testiotsikko 2</title>
            <link>https://example.com/2</link>
            <description>Testi kuvaus 2</description>
            <pubDate>Fri, 15 Nov 2024 13:00:00 GMT</pubDate>
        </item>
    </channel>
</rss>"""
