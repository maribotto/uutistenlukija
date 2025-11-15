#!/usr/bin/env python3
"""
Uutislukija - HS & YLE
Lukee uudet uutiset ääneen Piper TTS:llä
Cross-platform: Windows, macOS, Linux
"""

import feedparser
import subprocess
import time
import json
import os
import sys
import platform
import tempfile
from pathlib import Path
from datetime import datetime
from config import RSS_FEEDS, CHECK_INTERVAL

# Tunnista käyttöjärjestelmä
SYSTEM = platform.system()  # 'Windows', 'Darwin' (macOS), 'Linux'

# Projektin juurihakemisto
BASE_DIR = Path(__file__).parent.resolve()

# Piper TTS polut (dynaamiset)
if SYSTEM == "Windows":
    PIPER_EXECUTABLE = BASE_DIR / "piper" / "piper.exe"
elif SYSTEM == "Darwin":  # macOS
    PIPER_EXECUTABLE = BASE_DIR / "piper" / "piper"
else:  # Linux
    PIPER_EXECUTABLE = BASE_DIR / "piper" / "piper"

PIPER_MODEL = BASE_DIR / "fi_FI-asmo-medium.onnx"
READ_ARTICLES_FILE = BASE_DIR / "read_articles.json"

class NewsReader:
    def __init__(self):
        self.read_articles = self.load_read_articles()

    def load_read_articles(self):
        """Lataa jo luettujen artikkeleiden lista"""
        if READ_ARTICLES_FILE.exists():
            with open(READ_ARTICLES_FILE, 'r', encoding='utf-8') as f:
                return set(json.load(f))
        return set()

    def save_read_articles(self):
        """Tallenna luettujen artikkeleiden lista"""
        with open(READ_ARTICLES_FILE, 'w', encoding='utf-8') as f:
            json.dump(list(self.read_articles), f, ensure_ascii=False, indent=2)

    def play_audio_file(self, audio_file):
        """Toista äänitiedosto (cross-platform)"""
        try:
            if SYSTEM == "Windows":
                # Windows: käytä winsound tai PowerShell
                import winsound
                winsound.PlaySound(str(audio_file), winsound.SND_FILENAME)
            elif SYSTEM == "Darwin":  # macOS
                # macOS: käytä afplay
                subprocess.run(['afplay', str(audio_file)], check=True)
            else:  # Linux
                # Linux: käytä aplay
                subprocess.run(['aplay', '-q', str(audio_file)],
                             stdout=subprocess.DEVNULL,
                             stderr=subprocess.DEVNULL,
                             check=True)
        except Exception as e:
            print(f"Virhe äänen toistossa: {e}")

    def speak_finnish(self, text):
        """Lausu teksti suomeksi Piper TTS:llä (cross-platform)"""
        try:
            # Puhdista teksti
            clean_text = text.replace('\n', ' ').strip()

            # Luo väliaikainen WAV-tiedosto
            with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as tmp_file:
                tmp_path = tmp_file.name

            # Generoi puhe Piperillä
            with subprocess.Popen(
                [str(PIPER_EXECUTABLE), '--model', str(PIPER_MODEL), '--output_file', tmp_path],
                stdin=subprocess.PIPE,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            ) as piper:
                piper.communicate(input=clean_text.encode('utf-8'))

            # Toista äänitiedosto
            self.play_audio_file(tmp_path)

            # Poista väliaikainen tiedosto
            try:
                os.unlink(tmp_path)
            except:
                pass

        except Exception as e:
            print(f"Virhe puhesynteesissa: {e}")

    def is_today(self, entry):
        """Tarkista onko uutinen tältä päivältä"""
        try:
            # Kokeile hakea julkaisuaika
            if hasattr(entry, 'published_parsed') and entry.published_parsed:
                pub_time = datetime(*entry.published_parsed[:6])
            elif hasattr(entry, 'updated_parsed') and entry.updated_parsed:
                pub_time = datetime(*entry.updated_parsed[:6])
            else:
                # Jos aikaleimaa ei ole, oletetaan että on tältä päivältä
                return True

            # Tarkista onko sama päivä
            today = datetime.now().date()
            return pub_time.date() == today
        except:
            # Jos virhe, oletetaan että on tältä päivältä
            return True

    def fetch_and_read_news(self, initial_run=False):
        """Hae RSS-feedit ja lue uudet uutiset"""
        try:
            if initial_run:
                print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Luetaan tämän päivän uutiset...")
            else:
                print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Haetaan uutisia...")

            total_new_articles = 0

            for feed_info in RSS_FEEDS:
                feed_name = feed_info['name']
                feed_url = feed_info['url']

                print(f"\nTarkistetaan: {feed_name}")

                feed = feedparser.parse(feed_url)

                if feed.bozo:
                    print(f"  Virhe feedin lukemisessa: {feed.bozo_exception}")
                    continue

                new_articles_count = 0

                for entry in reversed(feed.entries):  # Vanhin ensin
                    article_id = entry.get('id', entry.get('link', ''))

                    # Ensimmäisellä kerralla: lue vain tämän päivän uutiset
                    if initial_run and not self.is_today(entry):
                        continue

                    if article_id not in self.read_articles:
                        new_articles_count += 1
                        total_new_articles += 1
                        title = entry.get('title', 'Ei otsikkoa')

                        print(f"  Uusi: {title}")

                        # Lausu lähde ja otsikko
                        self.speak_finnish(f"{feed_name}. {title}")

                        # Lausu tiivistelmä jos saatavilla
                        if 'summary' in entry:
                            summary = entry.summary[:500]  # Rajoita pituutta
                            self.speak_finnish(summary)

                        # Merkitse luetuksi
                        self.read_articles.add(article_id)
                        self.save_read_articles()

                        # Pieni tauko artikkeleiden välissä
                        time.sleep(2)

                if new_articles_count == 0:
                    print(f"  Ei uusia uutisia.")
                else:
                    print(f"  {new_articles_count} uutta uutista.")

            if total_new_articles == 0:
                print("\nEi uusia uutisia mistään lähteestä.")
            else:
                print(f"\nYhteensä {total_new_articles} uutta uutista.")

        except Exception as e:
            print(f"Virhe uutisten haussa: {e}")

    def check_requirements(self):
        """Tarkista että Piper ja malli ovat asennettu"""
        errors = []

        if not PIPER_EXECUTABLE.exists():
            errors.append(f"❌ Piper TTS ei löydy: {PIPER_EXECUTABLE}")
            errors.append(f"   Lataa Piper osoitteesta: https://github.com/rhasspy/piper/releases")

        if not PIPER_MODEL.exists():
            errors.append(f"❌ Äänimalli ei löydy: {PIPER_MODEL}")
            errors.append(f"   Lataa malli osoitteesta: https://huggingface.co/AsmoKoskinen/Piper_Finnish_Model")

        if errors:
            print("\n".join(errors))
            print("\nKatso asennusohjeet: README.md")
            sys.exit(1)

    def run(self):
        """Pääsilmukka"""
        print(f"Uutislukija käynnistetty (HS & YLE)")
        print(f"Käyttöjärjestelmä: {SYSTEM}")
        print(f"RSS-feedit:")
        for feed in RSS_FEEDS:
            print(f"  - {feed['name']}")
        print(f"Tarkistusväli: {CHECK_INTERVAL} sekuntia")
        print("-" * 50)

        # Tarkista vaatimukset
        self.check_requirements()

        try:
            # Ensimmäisellä kerralla: lue tämän päivän uutiset
            self.fetch_and_read_news(initial_run=True)

            print("\n" + "=" * 50)
            print("Aloitetaan uutisten vahtiminen...")
            print("=" * 50)

            # Sen jälkeen looppaa ja tarkista uusia
            while True:
                print(f"\nOdotetaan {CHECK_INTERVAL} sekuntia...")
                time.sleep(CHECK_INTERVAL)
                self.fetch_and_read_news(initial_run=False)
        except KeyboardInterrupt:
            print("\n\nLopetetaan...")
            self.save_read_articles()

if __name__ == "__main__":
    reader = NewsReader()
    reader.run()
