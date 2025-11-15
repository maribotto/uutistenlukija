"""
Integraatiotestit Piper TTS:lle
"""
import pytest
import subprocess
import tempfile
import os
from pathlib import Path

# Projektin tiedostot
import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
import uutistenlukija

@pytest.fixture
def piper_available():
    """Tarkista onko Piper asennettu"""
    return uutistenlukija.PIPER_EXECUTABLE.exists()

@pytest.fixture
def voice_model_available():
    """Tarkista onko äänimalli asennettu"""
    return uutistenlukija.PIPER_MODEL.exists()

def test_piper_executable_exists(piper_available):
    """Testaa että Piper executable on olemassa"""
    if not piper_available:
        pytest.skip("Piper ei ole asennettu")

    assert uutistenlukija.PIPER_EXECUTABLE.exists()
    assert uutistenlukija.PIPER_EXECUTABLE.is_file()

def test_voice_model_exists(voice_model_available):
    """Testaa että äänimalli on olemassa"""
    if not voice_model_available:
        pytest.skip("Äänimalli ei ole asennettu")

    assert uutistenlukija.PIPER_MODEL.exists()
    assert uutistenlukija.PIPER_MODEL.is_file()

@pytest.mark.slow
def test_piper_generates_speech(piper_available, voice_model_available):
    """Testaa että Piper generoi puhetta"""
    if not piper_available or not voice_model_available:
        pytest.skip("Piper tai äänimalli ei ole asennettu")

    # Luo väliaikainen tiedosto
    with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as tmp_file:
        tmp_path = tmp_file.name

    try:
        # Generoi puhe
        process = subprocess.Popen(
            [str(uutistenlukija.PIPER_EXECUTABLE), '--model', str(uutistenlukija.PIPER_MODEL),
             '--output_file', tmp_path],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        test_text = "Tämä on testi."
        process.communicate(input=test_text.encode('utf-8'), timeout=10)

        # Tarkista että WAV-tiedosto luotiin
        assert os.path.exists(tmp_path)
        assert os.path.getsize(tmp_path) > 0  # Ei tyhjä

    finally:
        # Poista väliaikainen tiedosto
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)

@pytest.mark.slow
def test_piper_version(piper_available):
    """Testaa että Piper version voidaan lukea"""
    if not piper_available:
        pytest.skip("Piper ei ole asennettu")

    result = subprocess.run(
        [str(uutistenlukija.PIPER_EXECUTABLE), '--version'],
        capture_output=True,
        text=True
    )

    # Piper saattaa palauttaa version tai help-tekstin
    # Tärkeintä on että komento toimii
    assert result.returncode in [0, 1]  # 0 = OK, 1 = käyttöohje

def test_platform_specific_paths():
    """Testaa että platform-spesifit polut on määritelty oikein"""
    import platform

    system = platform.system()

    if system == "Windows":
        assert str(uutistenlukija.PIPER_EXECUTABLE).endswith('.exe')
    else:
        assert not str(uutistenlukija.PIPER_EXECUTABLE).endswith('.exe')
