# Asennusohjeet

## Vaatimukset

- **Python 3.7+** (suositus: Python 3.10 tai 3.11)
- Tuetut käyttöjärjestelmät: Windows, macOS, Linux

**Testatut Python-versiot:**
- ✅ Python 3.10.17 - Täysin testattu (24/24 testiä)
- ✅ Python 3.11.14 - Täysin testattu (24/24 testiä)
- ✅ Python 3.12 - Toimii tuotannossa

Katso [PYTHON_VERSIONS.md](PYTHON_VERSIONS.md) täydelliset yhteensopivuustiedot.

---

## 0. Python-asennus (jos ei ole asennettu)

Jos sinulla ei ole Python:ia asennettuna, seuraa näitä ohjeita:

### Windows

**Vaihtoehto 1: Microsoft Store (suositus)**

1. Avaa Microsoft Store
2. Hae "Python 3.11" tai "Python 3.10"
3. Klikkaa **Get** / **Hanki**
4. Odota asennuksen valmistumista
5. Avaa Command Prompt ja tarkista: `python --version`

**Vaihtoehto 2: Python.org**

1. Mene osoitteeseen: https://www.python.org/downloads/windows/
2. Lataa **Python 3.11.x** tai **Python 3.10.x** (Windows installer 64-bit)
3. Aja asentaja
4. ✅ **TÄRKEÄ:** Valitse **"Add Python to PATH"** asennuksen alussa!
5. Klikkaa **Install Now**
6. Avaa Command Prompt ja tarkista: `python --version`

**Vaihtoehto 3: Winget (Windows Package Manager)**

```powershell
# Avaa PowerShell tai Command Prompt
winget install Python.Python.3.11
# tai
winget install Python.Python.3.10
```

### macOS

**Vaihtoehto 1: Homebrew (suositus)**

```bash
# Asenna Homebrew ensin (jos ei ole asennettu):
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Asenna Python
brew install python@3.11
# tai
brew install python@3.10

# Tarkista asennus
python3 --version
```

**Vaihtoehto 2: Python.org**

1. Mene osoitteeseen: https://www.python.org/downloads/macos/
2. Lataa **Python 3.11.x** tai **Python 3.10.x** (macOS 64-bit installer)
3. Avaa latautunut `.pkg` tiedosto
4. Seuraa asennusohjeita
5. Avaa Terminal ja tarkista: `python3 --version`

**Vaihtoehto 3: pyenv (kehittäjille)**

```bash
# Asenna pyenv
brew install pyenv

# Asenna Python
pyenv install 3.11.9
pyenv global 3.11.9

# Lisää .zshrc tai .bash_profile:
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.zshrc
echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.zshrc
echo 'eval "$(pyenv init -)"' >> ~/.zshrc
```

### Linux

**Ubuntu/Debian:**

```bash
# Päivitä pakettiluettelo
sudo apt update

# Asenna Python 3.11
sudo apt install python3.11 python3.11-venv python3.11-pip

# TAI Python 3.10
sudo apt install python3.10 python3.10-venv python3.10-pip

# Tarkista asennus
python3.11 --version
# tai
python3.10 --version

# Aseta oletukseksi (valinnainen)
sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.11 1
```

**Fedora/RHEL/CentOS:**

```bash
# Python 3.11
sudo dnf install python3.11 python3.11-pip

# Python 3.10
sudo dnf install python3.10 python3.10-pip

# Tarkista
python3.11 --version
```

**Arch Linux:**

```bash
# Python on yleensä jo asennettu
sudo pacman -S python python-pip

# Tarkista
python --version
```

**Mistä tahansa Linuxista (pyenv):**

```bash
# Asenna pyenv
curl https://pyenv.run | bash

# Lisää .bashrc tai .zshrc:
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
echo 'eval "$(pyenv init -)"' >> ~/.bashrc

# Lataa uudet asetukset
source ~/.bashrc

# Asenna Python
pyenv install 3.11.9
pyenv global 3.11.9
```

### Tarkista asennus

Kun Python on asennettu, tarkista että kaikki toimii:

**Windows:**
```powershell
python --version
python -m pip --version
```

**macOS/Linux:**
```bash
python3 --version
python3 -m pip --version
```

Pitäisi näyttää esim:
```
Python 3.11.9
pip 24.0 from ...
```

---

Uutislukija toimii **Windows**, **macOS** ja **Linux** käyttöjärjestelmissä.

## 1. Python-riippuvuudet

Asenna Python-kirjastot:

```bash
# Luo virtuaaliympäristö
python3 -m venv venv

# Aktivoi virtuaaliympäristö:
# Linux/macOS:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# Asenna riippuvuudet
pip install feedparser
```

## 2. Piper TTS asennus

### Linux (x86_64)

```bash
# Lataa Piper
wget https://github.com/rhasspy/piper/releases/download/2023.11.14-2/piper_linux_x86_64.tar.gz
tar -xzf piper_linux_x86_64.tar.gz
rm piper_linux_x86_64.tar.gz
```

### macOS (ARM64 / Apple Silicon)

```bash
# Lataa Piper
curl -L https://github.com/rhasspy/piper/releases/download/2023.11.14-2/piper_macos_arm64.tar.gz -o piper_macos_arm64.tar.gz
tar -xzf piper_macos_arm64.tar.gz
rm piper_macos_arm64.tar.gz
```

### macOS (x86_64 / Intel)

```bash
# Lataa Piper
curl -L https://github.com/rhasspy/piper/releases/download/2023.11.14-2/piper_macos_x64.tar.gz -o piper_macos_x64.tar.gz
tar -xzf piper_macos_x64.tar.gz
rm piper_macos_x64.tar.gz
```

### Windows

```powershell
# Lataa Piper manually osoitteesta:
# https://github.com/rhasspy/piper/releases/download/2023.11.14-2/piper_windows_amd64.zip

# Pura zip-tiedosto projektihakemistoon 'piper' -kansioon
```

## 3. Suomenkielinen äänimalli

Lataa AsmoKoskinen:n suomenkielinen äänimalli:

### Linux/macOS:

```bash
# Lataa äänimalli
wget https://huggingface.co/AsmoKoskinen/Piper_Finnish_Model/resolve/main/fi_FI-asmo-medium.onnx
wget https://huggingface.co/AsmoKoskinen/Piper_Finnish_Model/resolve/main/fi_FI-asmo-medium.onnx.json
```

### Windows (PowerShell):

```powershell
# Lataa äänimalli
Invoke-WebRequest -Uri "https://huggingface.co/AsmoKoskinen/Piper_Finnish_Model/resolve/main/fi_FI-asmo-medium.onnx" -OutFile "fi_FI-asmo-medium.onnx"
Invoke-WebRequest -Uri "https://huggingface.co/AsmoKoskinen/Piper_Finnish_Model/resolve/main/fi_FI-asmo-medium.onnx.json" -OutFile "fi_FI-asmo-medium.onnx.json"
```

## 4. Rakenne

Lopullisen hakemistorakenteen pitäisi näyttää tältä:

```
hesari-puhe/
├── hesari_rss_reader.py
├── piper/
│   └── piper (tai piper.exe Windowsissa)
├── fi_FI-asmo-medium.onnx
├── fi_FI-asmo-medium.onnx.json
└── venv/
```

## 5. Testaus

Testaa että kaikki toimii:

### Linux/macOS:

```bash
./venv/bin/python3 test_piper_speech.py
```

### Windows:

```powershell
venv\Scripts\python test_piper_speech.py
```

## 6. Käynnistys

### Linux/macOS:

```bash
./venv/bin/python3 hesari_rss_reader.py
```

### Windows:

```powershell
venv\Scripts\python hesari_rss_reader.py
```

Tai käytä mukana tulevaa käynnistysskriptiä:

### Linux/macOS:

```bash
./start_reader.sh
```

### Windows:

Luo `start_reader.bat` tiedosto:

```batch
@echo off
venv\Scripts\python hesari_rss_reader.py
pause
```

Sitten aja:

```powershell
start_reader.bat
```

## Äänientoisto

Ohjelma käyttää automaattisesti oikean käyttöjärjestelmän äänentoistokomentoa:

- **Linux**: `aplay`
- **macOS**: `afplay` (sisäänrakennettu)
- **Windows**: `winsound` (Python-moduuli, sisäänrakennettu)

Ei vaadi lisäasennuksia!

## Ongelmat?

Jos kohtaat ongelmia:

1. Tarkista että `piper` ja `fi_FI-asmo-medium.onnx` ovat oikeissa hakemistoissa
2. Varmista että Python-virtuaaliympäristö on aktivoitu
3. Linux: Tarkista että `aplay` on asennettu (`sudo apt install alsa-utils`)
