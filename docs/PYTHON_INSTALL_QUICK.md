# Python-asennus - Pika-ohjeet

## Windows

**Helpoin tapa:**
1. Avaa **Microsoft Store**
2. Hae "**Python 3.11**"
3. Paina **Hanki**
4. Valmis! ✅

**TAI komentoriviltä:**
```powershell
winget install Python.Python.3.11
```

## macOS

**Helpoin tapa (Homebrew):**
```bash
brew install python@3.11
```

Jos sinulla ei ole Homebrew:ia:
1. Avaa https://www.python.org/downloads/macos/
2. Lataa **Python 3.11** installer
3. Asenna se

## Linux

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install python3.11 python3.11-venv python3.11-pip
```

**Fedora:**
```bash
sudo dnf install python3.11 python3.11-pip
```

**Arch:**
```bash
sudo pacman -S python python-pip
```

## Tarkista että Python on asennettu

**Windows:**
```powershell
python --version
```

**macOS/Linux:**
```bash
python3 --version
```

Pitäisi näyttää jotain tyyliin: `Python 3.11.9` ✅

---

## Seuraavat vaiheet

Kun Python on asennettu, voit käynnistää Uutistenlukijan:

```bash
python3 kaynnista.py
```

Tämä komento asentaa automaattisesti kaikki muut tarvittavat komponentit!

---

Katso yksityiskohtaiset ohjeet: [INSTALL.md](INSTALL.md)
