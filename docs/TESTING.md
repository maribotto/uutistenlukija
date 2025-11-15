# Testauksen dokumentaatio

## Yleiskatsaus

Uutistenlukija-projekti sisältää kattavan automaattisen testisviitt joka varmistaa että kaikki komponentit toimivat odotetusti eri käyttöjärjestelmissä.

## Testien ajaminen

### Nopea käynnistys

```bash
python3 aja_testit.py
```

Tämä komento:
1. Tarkistaa että virtuaaliympäristö on olemassa
2. Asentaa pytest:in automaattisesti jos sitä ei ole
3. Ajaa kaikki nopeat testit (skippaaa verkko-testit)
4. Näyttää värillisen raportin tuloksista

### Eri testausvaihtosdot

```bash
# Kaikki testit (nopeat)
python3 aja_testit.py

# Kaikki testit mukaan lukien verkko-testit
python3 aja_testit.py -m ""

# Vain yksikkötestit
python3 aja_testit.py tests/unit/

# Vain integraatiotestit
python3 aja_testit.py tests/integration/

# Yksittäinen testitiedosto
python3 aja_testit.py tests/unit/test_config.py

# Yksittäinen testi
python3 aja_testit.py tests/unit/test_config.py::test_config_imports

# Verbose-tilassa
python3 aja_testit.py -v

# Näytä kaikki print-viestit
python3 aja_testit.py -s
```

## Testien rakenne

### Yksikkötestit (tests/unit/)

**test_config.py** - Konfiguraation testit:
- `test_config_imports` - Konfiguraation latautuminen
- `test_rss_feeds_structure` - RSS_FEEDS listan rakenne
- `test_check_interval` - CHECK_INTERVAL arvo
- `test_helsingin_sanomat_feed` - HS feed löytyy
- `test_yle_feed` - YLE feed löytyy

**test_newsreader.py** - NewsReader-luokan testit:
- `test_newsreader_init` - Alustus
- `test_load_read_articles_empty` - Tyhjän tiedoston lataus
- `test_load_read_articles_existing` - Olemassa olevan tiedoston lataus
- `test_save_read_articles` - Tallennuksen toiminta
- `test_is_today` - Päivämäärän tarkistus
- `test_is_today_no_date` - Päivämäärän tarkistus ilman aikaleimaa
- `TestPlatformDetection::test_system_variable_set` - Käyttöjärjestelmän tunnistus
- `TestPlatformDetection::test_piper_executable_path` - Piper-polun määrittely

### Integraatiotestit (tests/integration/)

**test_rss_feeds.py** - RSS-feedien testit:
- `test_helsingin_sanomat_feed_accessible` - HS feed saavutettavissa (verkko)
- `test_yle_feed_accessible` - YLE feed saavutettavissa (verkko)
- `test_all_feeds_valid` - Kaikki feedit valideja (verkko)
- `test_mock_rss_feed_parsing` - Mock-datan parsiminen

**test_piper_tts.py** - Piper TTS:n testit:
- `test_piper_executable_exists` - Piper-binääri on olemassa
- `test_voice_model_exists` - Äänimalli on olemassa
- `test_piper_generates_speech` - Puheen generointi toimii (hidas)
- `test_piper_version` - Version lukeminen (hidas)
- `test_platform_specific_paths` - Platform-spesifit polut oikein

**test_installation.py** - Asennuksen testit:
- `test_python_version` - Python-versio riittävä
- `test_venv_exists` - Virtuaaliympäristö olemassa
- `test_feedparser_installed` - feedparser asennettu
- `test_project_structure` - Projektin rakenne oikea
- `test_config_file_valid` - config.py validi
- `test_main_script_valid` - uutistenlukija.py validi
- `test_launcher_script_valid` - kaynnista.py validi ja executable

## Markerit

Testit käyttävät pytest-markereita ryhmittelyyn:

- `@pytest.mark.slow` - Hitaat testit (verkko, TTS)
- `@pytest.mark.unit` - Yksikkötestit
- `@pytest.mark.integration` - Integraatiotestit

### Markereiden käyttö

```bash
# Aja vain hitaat testit
python3 aja_testit.py -m "slow"

# Aja kaikki paitsi hitaat
python3 aja_testit.py -m "not slow"

# Aja vain yksikkötestit
python3 aja_testit.py -m "unit"
```

## Fixtures

**conftest.py** sisältää jaettuja pytest fixtureja:

- `base_dir` - Projektin juurihakemisto
- `test_data_dir` - Testidatan hakemisto
- `mock_rss_feed` - Mock RSS feed XML-data

## Testien kirjoittaminen

### Uuden yksikkötestin lisääminen

1. Luo testi `tests/unit/test_ominaisuus.py`
2. Käytä descriptive nimiä: `test_feature_does_something`
3. Käytä fixtureja aina kun mahdollista
4. Mockaa ulkoiset riippuvuudet

```python
import pytest
from unittest.mock import Mock, patch

def test_example_feature():
    """Testaa esimerkkiominaisuutta"""
    # Arrange
    test_data = "test"

    # Act
    result = function_to_test(test_data)

    # Assert
    assert result == expected_value
```

### Uuden integraatiotestin lisääminen

1. Luo testi `tests/integration/test_ominaisuus.py`
2. Merkitse verkko-testit `@pytest.mark.slow`
3. Skippaaa testit jos riippuvuudet puuttuvat

```python
import pytest

@pytest.mark.slow
def test_network_feature():
    """Testaa verkko-ominaisuutta"""
    # Testi joka vaatii verkkoyhteyttä
    pass

def test_local_integration(piper_available):
    """Testaa lokaalista integraatiota"""
    if not piper_available:
        pytest.skip("Piper ei ole asennettu")

    # Testi joka vaatii Piper:in
    pass
```

## CI/CD

Testit voidaan ajaa jatkuvassa integraatiossa:

```yaml
# .github/workflows/test.yml
name: Tests
on: [push, pull_request]

jobs:
  test:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, windows-latest, macos-latest]
        python-version: ['3.7', '3.8', '3.9', '3.10', '3.11', '3.12']

    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: ${{ matrix.python-version }}

      - name: Run tests
        run: |
          python3 -m venv venv
          python3 aja_testit.py -m "not slow"
```

## Testikattavuus

Jos haluat nähdä testikattavuuden:

```bash
# Asenna coverage
./venv/bin/pip install coverage

# Aja testit coverage-työkalulla
./venv/bin/coverage run -m pytest tests/

# Näytä raportti
./venv/bin/coverage report

# Luo HTML-raportti
./venv/bin/coverage html
# Avaa htmlcov/index.html selaimessa
```

## Yleisiä ongelmia

### Testit epäonnistuvat verkko-virheisiin

Verkko-testit on merkitty `@pytest.mark.slow`. Aja testit ilman niitä:

```bash
python3 aja_testit.py -m "not slow"
```

### Piper TTS testit skippaavat

Piper TTS ja äänimalli on asennettava ensin:

```bash
python3 kaynnista.py --check-only
```

### Import-virheet

Varmista että olet projektin juurihakemistossa ja venv on aktivoitu:

```bash
cd /path/to/uutistenlukija
python3 aja_testit.py  # aja_testit.py hoitaa venv:in
```

## Lisätietoja

- pytest dokumentaatio: https://docs.pytest.org/
- unittest.mock: https://docs.python.org/3/library/unittest.mock.html
- Test-driven development: https://en.wikipedia.org/wiki/Test-driven_development
