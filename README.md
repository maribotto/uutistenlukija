# Suomalainen uutislukija (HS & YLE)

Sovellus vahtii Helsingin Sanomien ja YLE Uutisten RSS-feedejä ja lukee uudet uutiset ääneen Piper TTS:llä (neuraalinen puhesyntetisaattori).

**Cross-platform:** Toimii Windows, macOS ja Linux järjestelmissä! 🌍

## Ominaisuudet

✅ Lukee Helsingin Sanomien ja YLE:n uutiset ääneen

✅ Lukee tämän päivän uutiset käynnistyksessä

✅ Vahtii RSS-feedejä ja lukee uudet uutiset automaattisesti

✅ Laadukas neuraalinen puhesynteesi (Piper TTS)

✅ Toimii kaikissa käyttöjärjestelmissä (Windows, macOS, Linux)

✅ Täysin offline - ei vaadi nettiyhteyttä toiston aikana

✅ **Automaattinen asennus** - lataa ja asentaa kaiken tarvittavan ensimmäisellä kerralla!

✅ **Kattavat automaattiset testit** - 29 testiä varmistavat että kaikki toimii

✅ **Graafinen TUI-käyttöliittymä** - helppokäyttöinen terminaali-valikkojärjestelmä

✅ **Tuplaklikkaus-yhteensopiva** - käynnistä tiedostosta ilman komentoriviä!

## 🚀 Pika-aloitus (SUOSITELTU)

**Vaatimukset:** Python 3.7+ (suositus: Python 3.10 tai 3.11)

<details>
<summary>❓ Eikö sinulla ole Python:ia?</summary>

### Asenna Python:

**Windows:** Microsoft Store → Hae "Python 3.11" → Hanki
**macOS:** `brew install python@3.11`
**Linux:** `sudo apt install python3.11 python3.11-venv`

📖 [Yksityiskohtaiset asennusohjeet →](docs/PYTHON_INSTALL_QUICK.md) | [Kaikki vaihtoehdot →](docs/INSTALL.md)

</details>

<details>
<summary>📋 Testatut Python-versiot</summary>

| Versio | Status | Testit |
|--------|--------|--------|
| Python 3.10 | ✅ TOIMII | 24/24 |
| Python 3.11 | ✅ TOIMII | 24/24 |
| Python 3.12 | ✅ TOIMII | Manuaalisesti testattu |

Katso [docs/PYTHON_VERSIONS.md](docs/PYTHON_VERSIONS.md) tarkemmat tiedot.
</details>

### Kaikki käyttöjärjestelmät (Windows, macOS, Linux):

```bash
# Lataa projekti ja siirry hakemistoon
cd uutistenlukija

# Käynnistä graafisella valikolla (SUOSITUS):
python3 kaynnista_helppo.py

# TAI käynnistä suoraan:
python3 kaynnista.py
```

Tämä on kaikki mitä tarvitset! Skripti:
- Luo virtuaaliympäristön
- Asentaa Python-riippuvuudet (feedparser, curses)
- Lataa Piper TTS:n (oikea versio käyttöjärjestelmällesi)
- Lataa suomenkielisen äänimallin
- Käynnistää ohjelman (tai näyttää graafisen valikon)

**Ensimmäinen käynnistys kestää ~1-2 minuuttia** (lataa ~60 MB). Sen jälkeen käynnistys on nopea.

👵 **Aloittelija?** Katso: [docs/KÄYTTÖOHJE_MUMMOLLE.md](docs/KÄYTTÖOHJE_MUMMOLLE.md) - yksinkertainen opas suomeksi!

## 📖 Manuaalinen asennus (vaihtoehtoinen)

Jos haluat asentaa komponentit itse, katso: **[docs/INSTALL.md](docs/INSTALL.md)**

## Käyttö

### 🖱️ HELPOIN: Tuplaklikkaa tiedostoa! (SUOSITUS)

**Windows:**
- Mene `windows/` kansioon
- Tuplaklikkaa: `kaynnista_helppo.bat`

**macOS:**
- Mene `macos/` kansioon
- Tuplaklikkaa: `Kaynnista_Uutislukija.command`

**Linux:**
- Mene `linux/` kansioon
- Tuplaklikkaa: `Uutislukija.desktop` (tai `kaynnista_helppo.sh`)

Ensimmäisellä kerralla käyttöjärjestelmä saattaa kysyä luvan skriptin suorittamiseen.

### 🎯 Graafinen TUI-valikko (Komentorivi):

**Windows (PowerShell TUI):**
```powershell
kaynnista_helppo.bat
# TAI
python kaynnista_helppo.py
```

**Linux/macOS (Curses TUI):**
```bash
python3 kaynnista_helppo.py
```

**Uusi!** Helppokäyttöinen graafinen terminaali-valikkojärjestelmä:
- 📋 Selkeä valikko nuolinäppäimillä navigoitavaksi
- 🚀 Käynnistä uutislukija
- ⚙️ Tarkista asennus
- 🧪 Aja testit
- 📖 Näytä ohjeet
- 🪟 **Windows**: Käyttää natiiveja PowerShell-värejä ja -laatikoita
- 🐧 **Linux/macOS**: Käyttää curses-kirjastoa
- 💻 **Fallback**: Yksinkertainen teksti-valikko jos grafiikka ei toimi

👵 **Erityisen helppo aloittelijoille!** Katso: [docs/KÄYTTÖOHJE_MUMMOLLE.md](docs/KÄYTTÖOHJE_MUMMOLLE.md)

### Suora käynnistys:

```bash
python3 kaynnista.py
```

Toimii kaikissa käyttöjärjestelmissä! 🎉

### Vaihtoehtoiset tavat:

**Linux/macOS:**
```bash
./venv/bin/python3 uutistenlukija.py
# tai
./scripts/start_reader.sh
```

**Windows:**
```powershell
venv\Scripts\python uutistenlukija.py
# tai
scripts\start_reader.bat
```

### Sovellus:
- Lukee tämän päivän uutiset käynnistyksessä
- Tarkistaa RSS-feedit 5 minuutin välein
- Lukee uudet uutiset ääneen suomeksi
- Pitää kirjaa jo luetuista uutisista (`read_articles.json`)
- Pysäytä: Ctrl+C

## Testit

Projekti sisältää kattavan testisviitin. Testit ajetaan automaattisesti yhdellä komennolla:

```bash
python3 scripts/aja_testit.py
```

Tämä skripti:
- Asentaa pytest:in automaattisesti
- Ajaa kaikki testit (paitsi hitaat verkko-testit)
- Näyttää selkeän raportin tuloksista

### Testien tyypit

**Yksikkötestit** (tests/unit/):
- Konfiguraation testit
- NewsReader-luokan testit
- Platform detection -testit

**Integraatiotestit** (tests/integration/):
- RSS-feedien testit
- Piper TTS:n testit
- Asennuksen testit

### Testien ajaminen

```bash
# Kaikki testit (nopeat)
python3 scripts/aja_testit.py

# Kaikki testit mukaan lukien hitaat (verkko-testit)
python3 scripts/aja_testit.py -m ""

# Vain yksikkötestit
python3 scripts/aja_testit.py tests/unit/

# Vain integraatiotestit
python3 scripts/aja_testit.py tests/integration/

# Yksittäinen testi
python3 scripts/aja_testit.py tests/unit/test_config.py

# Verbose-tilassa
python3 scripts/aja_testit.py -v
```

## Asetukset

Muokkaa tiedostoa `config.py`:

- `RSS_FEEDS`: Lista RSS-feededeistä (oletus: HS ja YLE)
- `CHECK_INTERVAL`: Tarkistusväli sekunneissa (oletus: 300)

Voit lisätä uusia RSS-feedejä lisäämällä ne `RSS_FEEDS` listaan.

## Uutislähteet

Oletuksena käytössä:
- **Helsingin Sanomat** - Tuoreimmat uutiset
- **YLE Uutiset** - Viimeisimmät uutiset

Voit lisätä tai poistaa feedejä muokkaamalla `RSS_FEEDS` listaa koodissa.

## Projektin rakenne

```
uutistenlukija/
├── kaynnista.py                 # ⭐ ALOITA TÄSTÄ - Automaattinen asennus ja käynnistys
├── kaynnista_helppo.py          # Graafinen TUI-valikko (kaikki OS)
├── uutislukija_tui.py           # Linux/macOS Curses TUI
├── uutistenlukija.py            # Pääohjelma
├── config.py                    # Konfiguraatio
├── requirements.txt             # Python-riippuvuudet
├── pytest.ini                   # Pytest-konfiguraatio
├── README.md                    # Tämä tiedosto
├── LICENSE                      # Lisenssitiedot
├── windows/                     # 🪟 Windows-käynnistimet
│   ├── kaynnista_helppo.bat     # 🖱️ Tuplaklikkaa tätä!
│   └── kaynnista_tui.ps1        # PowerShell TUI
├── macos/                       # 🍎 macOS-käynnistimet
│   └── Kaynnista_Uutislukija.command # 🖱️ Tuplaklikkaa tätä!
├── linux/                       # 🐧 Linux-käynnistimet
│   ├── Uutislukija.desktop      # 🖱️ Tuplaklikkaa tätä!
│   └── kaynnista_helppo.sh      # 🖱️ Tai tätä
├── docs/                        # Dokumentaatio
│   ├── INSTALL.md               # Manuaaliset asennusohjeet
│   ├── PLATFORM_SUPPORT.md      # Cross-platform dokumentaatio
│   ├── PYTHON_INSTALL_QUICK.md  # Python-asennus pika-ohjeet
│   ├── PYTHON_VERSIONS.md       # Python-versioiden yhteensopivuus
│   └── KÄYTTÖOHJE_MUMMOLLE.md   # Yksinkertainen opas aloittelijoille
├── scripts/                     # Työkaluskriptit
│   ├── aja_testit.py            # ⭐ Testien suoritus
│   ├── tarkista_asennus.py      # Asennuksen tarkistus
│   ├── testaa_python_versiot.py # Python-versiotestit
│   ├── tarkista_tui.py          # TUI-integraation tarkistus
│   ├── test_tui_demo.py         # TUI-demo
│   ├── start_reader.sh          # Vaihtoehtoinen käynnistin (Linux/macOS)
│   ├── start_reader.bat         # Vaihtoehtoinen käynnistin (Windows)
│   └── read_one_news.py         # Yksittäisen uutisen lukija
├── tests/                      # Testit
│   ├── conftest.py             # Pytest fixtures
│   ├── unit/                   # Yksikkötestit
│   │   ├── test_config.py      # Konfiguraation testit
│   │   └── test_newsreader.py  # NewsReader-luokan testit
│   ├── integration/            # Integraatiotestit
│   │   ├── test_rss_feeds.py   # RSS-feedien testit
│   │   ├── test_piper_tts.py   # Piper TTS:n testit
│   │   └── test_installation.py # Asennuksen testit
│   └── *.py                    # Vanhat testiskriptit (legacy)
├── venv/                       # Python virtuaaliympäristö (luodaan automaattisesti)
├── piper/                      # Piper TTS binääri (ladataan automaattisesti)
├── fi_FI-asmo-medium.onnx      # Suomenkielinen äänimalli (ladataan automaattisesti)
└── read_articles.json          # Jo luetut artikkelit (luodaan automaattisesti)
```

## Piper TTS käyttö

Voit myös käyttää Piper TTS:ää suoraan:

```bash
# Lue teksti
echo "Tervetuloa" | ./piper/piper --model fi_FI-asmo-medium.onnx --output_file - | aplay

# Tallenna tiedostoon
echo "Hei maailma" | ./piper/piper --model fi_FI-asmo-medium.onnx --output_file output.wav

# Lue tekstitiedosto
cat teksti.txt | ./piper/piper --model fi_FI-asmo-medium.onnx --output_file - | aplay
```

## Miksi Piper TTS?

Piper on neuraalinen puhesyntetisaattori joka kuulostaa paljon luonnollisemmalta kuin perinteiset TTS-moottorit (kuten eSpeak-NG). Se on:
- Nopea
- Laadukas
- Kevyt (ei vaadi GPU:ta)
- Täysin offline (ei tarvitse nettiyhteyttä)

## Lisenssi

Tämä projekti on lisensoitu **CC-BY-NC-4.0** lisenssillä (Creative Commons Attribution-NonCommercial 4.0).

### Mitä tämä tarkoittaa?

✅ Voit vapaasti:
- Käyttää projektia henkilökohtaisesti
- Jakaa ja muokata koodia
- Oppia ja tutkia

❌ Et voi:
- Käyttää projektia kaupallisiin tarkoituksiin
- Myydä tai ansaita rahaa tällä

### Attribuutio

Projekti käyttää seuraavia komponentteja:

- **Piper TTS** by Rhasspy (MIT License)
- **Finnish Voice Model** by AsmoKoskinen (CC-BY-NC-4.0)
- **feedparser** (BSD-2-Clause)

Katso lisätiedot: [LICENSE](LICENSE)
