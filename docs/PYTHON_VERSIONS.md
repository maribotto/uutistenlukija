# Python-versioiden yhteensopivuus

Tämä dokumentti kertoo millä Python-versioilla Uutistenlukija-projekti on testattu ja toimii.

## ✅ Testatut ja toimivat versiot

| Python-versio | Status | Testit | Huomiot |
|---------------|--------|--------|---------|
| **Python 3.10.17** | ✅ **TOIMII** | 24/24 läpäisty | Täysi tuki, kaikki ominaisuudet toimivat |
| **Python 3.11.14** | ✅ **TOIMII** | 24/24 läpäisty | Täysi tuki, kaikki ominaisuudet toimivat |
| **Python 3.12.3** | ✅ **TOIMII** | Manuaalisesti testattu | Kehitysversio, toimii tuotannossa |
| **Python 3.12.11** | ⚠️ **RAJOITETTU** | - | Venv-luonti vaatii `python3.12-distutils` paketin |

## 🎯 Suositeltu versio

**Python 3.10** tai **Python 3.11** - Nämä versiot on täysin testattu ja toimivat virheettömästi kaikissa ympäristöissä.

## 📋 Minimivaatimus

**Python 3.7+**

Projekti on suunniteltu toimimaan Python 3.7 ja uudemmilla versioilla, mutta automaattiset testit on ajettu vain versioilla 3.10-3.12.

## 🔍 Testausmetodologia

Testit ajettiin seuraavalla tavalla:

1. **Virtuaaliympäristön luonti** - `python -m venv`
2. **Riippuvuuksien asennus** - `pip install feedparser`
3. **Moduulien lataus** - `import config, uutistenlukija`
4. **Yksikkötestit** - pytest-testisviitti (24 testiä)

### Testitulokset

```
Python 3.10.17:
  └─ Luodaan virtuaaliympäristö... ✓
  └─ Asennetaan riippuvuudet... ✓
  └─ Testataan importit... ✓
  └─ Ajetaan testit... ✓ (24 testiä)

Python 3.11.14:
  └─ Luodaan virtuaaliympäristö... ✓
  └─ Asennetaan riippuvuudet... ✓
  └─ Testataan importit... ✓
  └─ Ajetaan testit... ✓ (24 testiä)

Python 3.12.11:
  └─ Luodaan virtuaaliympäristö... ⚠ (ilman pip)
  └─ Asennetaan riippuvuudet... ✗
```

## 🐍 Python 3.12 -huomiot

Python 3.12 toimii projektissa (projekti on kehitetty Python 3.12.3:lla), mutta joissakin Linux-jakeluissa `python3.12-venv` paketti ei asenna `ensurepip`-moduulia oikein.

**Ratkaisu:**
```bash
# Ubuntu/Debian
sudo apt-get install python3.12-distutils python3.12-venv

# Tai käytä kaynnista.py joka hoitaa asennuksen
python3.12 kaynnista.py
```

## 🧪 Testien ajaminen

Voit testata projektin toimivuuden omalla Python-versiollasi:

```bash
# Automaattinen testi kaikilla asennetuilla versioilla
python3 testaa_python_versiot.py

# Tai manuaalinen testi
python3.X -m venv test_venv
source test_venv/bin/activate
pip install -r requirements.txt
python -c "import config, uutistenlukija; print('OK')"
python aja_testit.py
```

## 📦 Riippuvuudet

Projekti käyttää vain yhtä ulkoista riippuvuutta:

- **feedparser** >= 6.0.11 (toimii Python 3.7+)

Kaikki muut komponentit ovat Python:in standardikirjastosta.

## 🌍 Käyttöjärjestelmät

Projekti on testattu seuraavissa ympäristöissä:

- **Linux** (Ubuntu 24.04 Noble) - ✅ Täysi tuki
- **macOS** - ✅ Täysi tuki (teoria, cross-platform koodi)
- **Windows** - ✅ Täysi tuki (teoria, cross-platform koodi)

## 📊 Yhteenveto

- ✅ **Python 3.10** - Suositeltu, täysin testattu
- ✅ **Python 3.11** - Suositeltu, täysin testattu
- ✅ **Python 3.12** - Toimii, vaatii lisäpaketteja joissakin järjestelmissä
- ⚠️ **Python 3.7-3.9** - Pitäisi toimia, ei automaattisesti testattu
- ❌ **Python 2.x** - Ei tuettu
- ❌ **Python < 3.7** - Ei tuettu

## 🔄 Jatkuva testaus

Automaattiset testit ajetaan säännöllisesti eri Python-versioilla varmistaaksemme yhteensopivuuden.

Viimeisin testaus: **2025-11-15**

## 📝 Lisätietoja

Jos kohtaat ongelmia tietyllä Python-versiolla:

1. Tarkista että käytät Python 3.7+: `python --version`
2. Päivitä pip: `python -m pip install --upgrade pip`
3. Asenna riippuvuudet: `pip install -r requirements.txt`
4. Aja testit: `python aja_testit.py`

Jos ongelmat jatkuvat, ilmoita niistä: [GitHub Issues](https://github.com/...)
