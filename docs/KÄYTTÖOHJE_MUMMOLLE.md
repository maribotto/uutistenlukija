# 👵 Uutistenlukija - Käyttöohje isoäidille

## 📖 Mikä tämä on?

**Uutistenlukija** on ohjelma joka:
- 📰 Lukee **Helsingin Sanomien** ja **YLE:n** uutiset **ääneen suomeksi**
- 🔊 Käyttää tietokoneen kaiuttimia
- 🤖 Toimii automaattisesti - ei tarvitse kliksutella

## 🚀 SUPERNOPEA ALOITUS

### 🖱️ HELPOIN TAPA: Tuplaklikkaa!

**Windows:**
- Avaa uutistenlukija-kansio
- Mene **windows** -kansioon
- **Tuplaklikkaa** tiedostoa: `kaynnista_helppo.bat`
- Ohjelma käynnistyy automaattisesti!

**Mac:**
- Avaa uutistenlukija-kansio
- Mene **macos** -kansioon
- **Tuplaklikkaa** tiedostoa: `Kaynnista_Uutislukija.command`
- Ensimmäisellä kerralla Mac voi kysyä lupaa - salli!

**Linux:**
- Avaa uutistenlukija-kansio
- Mene **linux** -kansioon
- **Tuplaklikkaa** tiedostoa: `Uutislukija.desktop`
- TAI **tuplaklikkaa**: `kaynnista_helppo.sh`
- Ensimmäisellä kerralla järjestelmä voi kysyä lupaa - salli!

**SE ON KAIKKI!** 🎉

---

### ⌨️ VAIHTOEHTOINEN TAPA: Komentorivi

Jos tuplaklikkaus ei toimi, voit myös käyttää komentoriviä:

**1. Avaa "Komentorivi" tai "Terminal"**

- **Windows**: Paina `Win`-näppäintä, kirjoita "powershell", paina Enter
- **Mac**: Paina `Cmd + välilyönti`, kirjoita "terminal", paina Enter
- **Linux**: Paina `Ctrl + Alt + T`

**2. Kirjoita tämä komento ja paina Enter:**

**Windows:**
```
python kaynnista_helppo.py
```

**Mac/Linux:**
```
python3 kaynnista_helppo.py
```

---

## 📺 Mitä näytöllä tapahtuu?

Kun ajat ohjelman, näet **graafisen valikon**:

```
╔══════════════════════════════════════╗
║      🗞️  UUTISTENLUKIJA  🗞️         ║
║  Helsingin Sanomat & YLE             ║
╠══════════════════════════════════════╣

VALIKKO:

▶ 🚀 Käynnistä uutislukija
  ⚙️  Tarkista asennus
  🧪 Aja testit
  📖 Näytä ohjeet
  🚪 Lopeta

↑↓: Liiku | ENTER: Valitse | Q: Lopeta
```

### Käyttö:

1. **Nuolinäppäimet ↑↓** - Liiku valikossa
2. **Enter** - Valitse haluamasi kohta
3. **Q** - Lopeta

## 🎯 Mitä valikon kohdat tekevät?

### 🚀 Käynnistä uutislukija

**Tämä on tärkein! Valitse tämä ensimmäiseksi.**

Ohjelma:
1. Tarkistaa että kaikki on asennettu
2. Jos jotain puuttuu, lataa ja asentaa sen automaattisesti
3. Alkaa lukea uutiset ääneen!

**Ensimmäinen käynnistys:** Kestää 1-2 minuuttia (lataa ~60 MB)
**Seuraavat kerrat:** Käynnistyy heti!

### ⚙️ Tarkista asennus

Näyttää mitä on jo asennettu:
- ✓ = Asennettu
- ✗ = Puuttuu

### 🧪 Aja testit

Testaa että kaikki toimii kunnolla. Ei tarvitse joka kerta!

### 📖 Näytä ohjeet

Näyttää nämä ohjeet.

### 🚪 Lopeta

Sulkee ohjelman.

---

## ❓ Usein kysytyt kysymykset

### Miten pysäytän uutisten lukemisen?

Paina `Ctrl + C` (pidä Ctrl-näppäintä pohjassa ja paina C)

### En kuule ääntä!

1. Tarkista että kaiuttimet ovat päällä
2. Tarkista että äänenvoimakkuus ei ole nollassa
3. Tarkista että oikea äänilaite on valittuna

### Ohjelma näyttää "Python-komentoa ei löydy"

Sinun pitää asentaa Python ensin. Katso: [PYTHON_INSTALL_QUICK.md](docs/PYTHON_INSTALL_QUICK.md)

**Lyhyesti:**

- **Windows:** Microsoft Store → Hae "Python 3.11" → Hanki
- **Mac:** `brew install python@3.11`
- **Linux:** `sudo apt install python3.11`

### Haluanko vaihtaa uutislähdettä?

Tällä hetkellä lukee vain HS:n ja YLE:n uutisia. Muita lähteitä voi lisätä muokkaamalla `config.py` tiedostoa, mutta se on edistyneempää.

### Miten usein ohjelma tarkistaa uusia uutisia?

Joka 5. minuutti. Voit muuttaa tätä `config.py` tiedostossa.

---

## 💡 Vinkit

### Ensimmäinen käynnistys

Kun käynnistät ensimmäistä kertaa:
- Odota rauhassa 1-2 minuuttia
- Ohjelma lataa tarvittavat tiedostot
- Näet edistymispalkin
- **ÄLÄ keskeytä** kesken latauksen!

### Seuraavat käynnistykset

Sen jälkeen ohjelma käynnistyy muutamassa sekunnissa!

### Päivittäinen käyttö

1. Avaa komentorivi
2. Aja: `python3 kaynnista_helppo.py`
3. Valitse "Käynnistä uutislukija"
4. Kuuntele uutiset!
5. Pysäytä: `Ctrl + C`

---

## 🆘 Jos jokin menee pieleen

### "Komento ei löydy" virhe

Olet väärässä kansiossa. Siirry oikeaan:

```
cd polku/jossa/uutistenlukija/on
```

### "Python ei ole asennettu"

Asenna Python (katso yllä)

### Jokin muu ongelma

1. Kokeile ajaa: `python3 scripts/tarkista_asennus.py`
2. Kokeile ajaa: `python3 scripts/aja_testit.py`
3. Katso tarkemmat ohjeet: [README.md](README.md)

---

## 📞 Apua!

Jos tarvitset apua, kysy nuoremmalta sukupolvelta näyttämään tämä ohje! 😊

Tai katso yksityiskohtaisemmat ohjeet:
- [README.md](README.md) - Pääohje
- [docs/INSTALL.md](docs/INSTALL.md) - Asennusohjeet
- [docs/PYTHON_INSTALL_QUICK.md](docs/PYTHON_INSTALL_QUICK.md) - Python-asennus

---

## ❤️ Nauti uutisista!

Tehty rakkaudella, jotta kaikki voivat kuunnella uutiset. 🎧

**Hyvää kuuntelua!** 📻
