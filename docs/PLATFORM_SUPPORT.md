# Cross-Platform tuki

Uutislukija toimii nyt **Windows**, **macOS** ja **Linux** käyttöjärjestelmissä!

## Toteutus

### Käyttöjärjestelmän tunnistus

```python
import platform
SYSTEM = platform.system()  # 'Windows', 'Darwin' (macOS), 'Linux'
```

### Dynaamiset polut

```python
from pathlib import Path
BASE_DIR = Path(__file__).parent.resolve()

# Automaattinen binäärin valinta
if SYSTEM == "Windows":
    PIPER_EXECUTABLE = BASE_DIR / "piper" / "piper.exe"
elif SYSTEM == "Darwin":  # macOS
    PIPER_EXECUTABLE = BASE_DIR / "piper" / "piper"
else:  # Linux
    PIPER_EXECUTABLE = BASE_DIR / "piper" / "piper"
```

### Äänientoisto

Jokainen käyttöjärjestelmä käyttää omaa äänentoistoratkaisuaan:

#### Linux
- **Komento**: `aplay`
- **Asennus**: `sudo apt install alsa-utils` (useimmiten valmiiksi asennettu)

#### macOS
- **Komento**: `afplay`
- **Asennus**: Sisäänrakennettu macOS:ssä, ei vaadi asennusta

#### Windows
- **Moduuli**: `winsound` (Python stdlib)
- **Asennus**: Sisäänrakennettu Pythonissa, ei vaadi asennusta

### Koodiratkaisu

```python
def play_audio_file(self, audio_file):
    """Toista äänitiedosto (cross-platform)"""
    if SYSTEM == "Windows":
        import winsound
        winsound.PlaySound(str(audio_file), winsound.SND_FILENAME)
    elif SYSTEM == "Darwin":  # macOS
        subprocess.run(['afplay', str(audio_file)], check=True)
    else:  # Linux
        subprocess.run(['aplay', '-q', str(audio_file)],
                     stdout=subprocess.DEVNULL,
                     stderr=subprocess.DEVNULL,
                     check=True)
```

## Piper TTS binäärit

### Latausosoitteet (GitHub Releases)

**Linux (x86_64):**
```
https://github.com/rhasspy/piper/releases/download/2023.11.14-2/piper_linux_x86_64.tar.gz
```

**macOS (ARM64 / Apple Silicon):**
```
https://github.com/rhasspy/piper/releases/download/2023.11.14-2/piper_macos_arm64.tar.gz
```

**macOS (x86_64 / Intel):**
```
https://github.com/rhasspy/piper/releases/download/2023.11.14-2/piper_macos_x64.tar.gz
```

**Windows (AMD64):**
```
https://github.com/rhasspy/piper/releases/download/2023.11.14-2/piper_windows_amd64.zip
```

## Testatut alustat

✅ **Linux** - Testattu Ubuntu 22.04+
⏳ **macOS** - Ei vielä testattu (pitäisi toimia)
⏳ **Windows** - Ei vielä testattu (pitäisi toimia)

## Tiedossa olevat rajoitukset

### Linux
- Vaatii `aplay`:n (ALSA utils)
- Toimii kaikissa yleisimmissä distroissa

### macOS
- `afplay` on sisäänrakennettu
- Pitäisi toimia kaikissa macOS versioissa

### Windows
- `winsound` on sisäänrakennettu Pythonissa
- Toimii Windows 7+

## Riippuvuudet

### Python-kirjastot
- `feedparser` - RSS-feedien lukeminen

### Järjestelmäriippuvuudet
- **Linux**: `aplay` (alsa-utils paketti)
- **macOS**: ei lisäriippuvuuksia
- **Windows**: ei lisäriippuvuuksia

## Käynnistysskriptit

### Linux/macOS
- `start_reader.sh` - Bash-skripti
- Tarkistaa virtuaaliympäristön
- Käynnistää ohjelman

### Windows
- `start_reader.bat` - Batch-skripti
- Tarkistaa virtuaaliympäristön
- Käynnistää ohjelman

## Testausohjeet

Testaa että cross-platform toiminnallisuus toimii:

```bash
# Linux/macOS
./venv/bin/python3 test_quick.py

# Windows
venv\Scripts\python test_quick.py
```

Tämä testaa:
1. Käyttöjärjestelmän tunnistuksen
2. Piper TTS:n toiminnan
3. Äänientoiston
4. RSS-feedin lukemisen

## Kehitysideoita tulevaisuuteen

- [ ] ARM Linux tuki (Raspberry Pi)
- [ ] Android tuki (Termux)
- [ ] Automaattinen Piper-lataus asennuksen yhteydessä
- [ ] GUI versio (PyQt/Tkinter)
