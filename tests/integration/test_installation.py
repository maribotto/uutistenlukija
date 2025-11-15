"""
Integraatiotestit asennukselle
"""
import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

def test_python_version():
    """Testaa että Python-versio on riittävä"""
    assert sys.version_info >= (3, 7), "Python 3.7+ vaaditaan"

def test_venv_exists(base_dir):
    """Testaa että virtuaaliympäristö on olemassa"""
    venv_dir = base_dir / "venv"

    # Tämä testi ei vaadi venv:iä jos ajetaan CI:ssä
    if not venv_dir.exists():
        pytest.skip("Virtuaaliympäristöä ei ole luotu")

    assert venv_dir.exists()
    assert venv_dir.is_dir()

def test_feedparser_installed():
    """Testaa että feedparser on asennettu"""
    try:
        import feedparser
        assert True
    except ImportError:
        pytest.fail("feedparser ei ole asennettu")

def test_project_structure(base_dir):
    """Testaa että projektin rakenne on oikea"""
    required_files = [
        "kaynnista.py",
        "uutistenlukija.py",
        "config.py",
        "requirements.txt",
        "README.md",
        "LICENSE",
    ]

    for filename in required_files:
        file_path = base_dir / filename
        assert file_path.exists(), f"Tiedosto {filename} puuttuu"

    required_dirs = [
        "docs",
        "scripts",
        "tests",
    ]

    for dirname in required_dirs:
        dir_path = base_dir / dirname
        assert dir_path.exists(), f"Hakemisto {dirname} puuttuu"
        assert dir_path.is_dir()

def test_config_file_valid(base_dir):
    """Testaa että config.py on validi Python-tiedosto"""
    config_file = base_dir / "config.py"
    assert config_file.exists()

    # Yritä importata
    import config
    assert hasattr(config, 'RSS_FEEDS')
    assert hasattr(config, 'CHECK_INTERVAL')

def test_main_script_valid(base_dir):
    """Testaa että uutistenlukija.py on validi Python-tiedosto"""
    main_file = base_dir / "uutistenlukija.py"
    assert main_file.exists()

    # Yritä importata
    import uutistenlukija
    assert hasattr(uutistenlukija, 'NewsReader')

def test_launcher_script_valid(base_dir):
    """Testaa että kaynnista.py on validi Python-tiedosto"""
    launcher_file = base_dir / "kaynnista.py"
    assert launcher_file.exists()

    # Tarkista että tiedosto on executable (Unix)
    import platform
    if platform.system() != "Windows":
        import os
        assert os.access(launcher_file, os.X_OK), "kaynnista.py ei ole executable"
