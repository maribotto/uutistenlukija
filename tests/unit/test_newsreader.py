"""
Testit NewsReader-luokalle
"""
import pytest
import sys
import tempfile
import json
from pathlib import Path
from datetime import datetime
from unittest.mock import Mock, patch, MagicMock

# Import NewsReader
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
import uutistenlukija

def test_newsreader_init():
    """Testaa NewsReader alustus"""
    with patch('uutistenlukija.READ_ARTICLES_FILE', Path(tempfile.mktemp())):
        reader = uutistenlukija.NewsReader()
        assert reader.read_articles == set()

def test_load_read_articles_empty():
    """Testaa tyhjän read_articles tiedoston lataus"""
    with patch('uutistenlukija.READ_ARTICLES_FILE', Path(tempfile.mktemp())):
        reader = uutistenlukija.NewsReader()
        assert reader.read_articles == set()

def test_load_read_articles_existing():
    """Testaa olemassa olevan read_articles tiedoston lataus"""
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
        test_articles = ["article1", "article2", "article3"]
        json.dump(test_articles, f)
        temp_path = Path(f.name)

    try:
        with patch('uutistenlukija.READ_ARTICLES_FILE', temp_path):
            reader = uutistenlukija.NewsReader()
            assert reader.read_articles == set(test_articles)
    finally:
        temp_path.unlink()

def test_save_read_articles():
    """Testaa read_articles tallennuksen"""
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
        # Kirjoita tyhjä JSON-taulukko tiedostoon
        json.dump([], f)
        temp_path = Path(f.name)

    try:
        with patch('uutistenlukija.READ_ARTICLES_FILE', temp_path):
            reader = uutistenlukija.NewsReader()
            reader.read_articles = {"article1", "article2"}
            reader.save_read_articles()

            # Tarkista että tiedosto luotiin
            assert temp_path.exists()

            # Tarkista sisältö
            with open(temp_path, 'r') as f:
                saved_articles = set(json.load(f))
                assert saved_articles == reader.read_articles
    finally:
        if temp_path.exists():
            temp_path.unlink()

def test_is_today():
    """Testaa is_today metodin"""
    with patch('uutistenlukija.READ_ARTICLES_FILE', Path(tempfile.mktemp())):
        reader = uutistenlukija.NewsReader()

        # Tämän päivän entry
        today_entry = Mock()
        today_time = datetime.now().timetuple()[:6]
        today_entry.published_parsed = today_time
        assert reader.is_today(today_entry) == True

        # Eilisen entry
        yesterday_entry = Mock()
        yesterday_time = (datetime.now().year, datetime.now().month, datetime.now().day - 1, 12, 0, 0)
        yesterday_entry.published_parsed = yesterday_time
        yesterday_entry.updated_parsed = None
        assert reader.is_today(yesterday_entry) == False

def test_is_today_no_date():
    """Testaa is_today kun päivämäärää ei ole"""
    with patch('uutistenlukija.READ_ARTICLES_FILE', Path(tempfile.mktemp())):
        reader = uutistenlukija.NewsReader()

        # Entry ilman päivämäärää
        no_date_entry = Mock()
        no_date_entry.published_parsed = None
        no_date_entry.updated_parsed = None

        # Oletetaan että on tältä päivältä jos päivämäärää ei ole
        assert reader.is_today(no_date_entry) == True

class TestPlatformDetection:
    """Testit platform detection -toiminnallisuudelle"""

    def test_system_variable_set(self):
        """Testaa että SYSTEM muuttuja on asetettu"""
        assert hasattr(uutistenlukija, 'SYSTEM')
        assert uutistenlukija.SYSTEM in ['Windows', 'Darwin', 'Linux']

    def test_piper_executable_path(self):
        """Testaa että Piper executable polku on määritelty"""
        assert hasattr(uutistenlukija, 'PIPER_EXECUTABLE')
        assert isinstance(uutistenlukija.PIPER_EXECUTABLE, Path)
