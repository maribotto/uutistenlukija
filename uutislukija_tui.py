#!/usr/bin/env python3
"""
Uutistenlukija - TUI (Text User Interface)
Graafinen käyttöliittymä terminaaliin
"""

import curses
import sys
import time
import threading
from pathlib import Path
from datetime import datetime

# Värikoodit (fallback jos curses ei toimi)
class SimpleColors:
    GREEN = '\033[92m'
    BLUE = '\033[94m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    END = '\033[0m'

class UutislukijaTUI:
    def __init__(self):
        self.BASE_DIR = Path(__file__).parent.resolve()
        self.current_menu = 0
        self.menu_items = [
            "🚀 Käynnistä uutislukija",
            "⚙️  Tarkista asennus",
            "🧪 Aja testit",
            "📖 Näytä ohjeet",
            "🚪 Lopeta"
        ]
        self.status_messages = []
        self.is_running = False

    def add_status(self, message, level="INFO"):
        """Lisää statusviesti"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.status_messages.append(f"[{timestamp}] {level}: {message}")
        # Pidä vain viimeiset 100 viestiä
        if len(self.status_messages) > 100:
            self.status_messages.pop(0)

    def draw_header(self, stdscr, height, width):
        """Piirrä otsikko"""
        title = "🗞️  UUTISTENLUKIJA  🗞️"
        subtitle = "Helsingin Sanomat & YLE - Suomeksi puhuen"

        # Otsikko
        x = (width - len(title)) // 2
        stdscr.attron(curses.color_pair(1) | curses.A_BOLD)
        stdscr.addstr(1, x, title)
        stdscr.attroff(curses.color_pair(1) | curses.A_BOLD)

        # Alaotsikko
        x = (width - len(subtitle)) // 2
        stdscr.attron(curses.color_pair(2))
        stdscr.addstr(2, x, subtitle)
        stdscr.attroff(curses.color_pair(2))

        # Viiva
        stdscr.addstr(3, 2, "═" * (width - 4))

    def draw_menu(self, stdscr, height, width):
        """Piirrä valikko"""
        menu_y = 5

        stdscr.attron(curses.color_pair(3) | curses.A_BOLD)
        stdscr.addstr(menu_y, 4, "PÄÄVALIKKO")
        stdscr.attroff(curses.color_pair(3) | curses.A_BOLD)

        for idx, item in enumerate(self.menu_items):
            y = menu_y + 2 + idx
            if idx == self.current_menu:
                # Valittu vaihtoehto
                stdscr.attron(curses.color_pair(4) | curses.A_BOLD)
                stdscr.addstr(y, 4, f"▶ {item}")
                stdscr.attroff(curses.color_pair(4) | curses.A_BOLD)
            else:
                stdscr.addstr(y, 6, item)

    def draw_status_box(self, stdscr, height, width):
        """Piirrä status-laatikko"""
        box_y = height - 12
        box_height = 10

        # Laatikon otsikko
        stdscr.attron(curses.color_pair(3) | curses.A_BOLD)
        stdscr.addstr(box_y, 4, "📊 STATUS")
        stdscr.attroff(curses.color_pair(3) | curses.A_BOLD)

        # Laatikko
        for i in range(box_height - 2):
            y = box_y + 1 + i
            if y < height - 1:
                stdscr.addstr(y, 3, "│")
                stdscr.addstr(y, width - 4, "│")

        # Viestit (näytä viimeiset 6)
        visible_messages = self.status_messages[-6:]
        for idx, msg in enumerate(visible_messages):
            y = box_y + 2 + idx
            if y < height - 2:
                # Leikkaa viesti jos liian pitkä
                max_len = width - 10
                if len(msg) > max_len:
                    msg = msg[:max_len-3] + "..."

                # Väritä viesti tason mukaan
                if "ERROR" in msg:
                    stdscr.attron(curses.color_pair(5))
                elif "SUCCESS" in msg or "✓" in msg:
                    stdscr.attron(curses.color_pair(4))
                elif "WARNING" in msg:
                    stdscr.attron(curses.color_pair(6))
                else:
                    stdscr.attron(curses.color_pair(2))

                stdscr.addstr(y, 5, msg)
                stdscr.attroff(curses.color_pair(2))
                stdscr.attroff(curses.color_pair(4))
                stdscr.attroff(curses.color_pair(5))
                stdscr.attroff(curses.color_pair(6))

    def draw_footer(self, stdscr, height, width):
        """Piirrä alatunniste"""
        footer_y = height - 1

        controls = "↑↓: Liiku | ENTER: Valitse | Q: Lopeta"
        x = (width - len(controls)) // 2

        stdscr.attron(curses.color_pair(2))
        stdscr.addstr(footer_y, x, controls)
        stdscr.attroff(curses.color_pair(2))

    def draw_screen(self, stdscr):
        """Piirrä koko näyttö"""
        height, width = stdscr.getmaxyx()

        stdscr.clear()

        # Piirrä komponentit
        self.draw_header(stdscr, height, width)
        self.draw_menu(stdscr, height, width)
        self.draw_status_box(stdscr, height, width)
        self.draw_footer(stdscr, height, width)

        stdscr.refresh()

    def show_message_box(self, stdscr, title, message, lines=None):
        """Näytä viesti-ikkuna"""
        height, width = stdscr.getmaxyx()

        if lines is None:
            lines = message.split('\n')

        box_width = min(width - 10, max(len(line) for line in lines) + 4, 70)
        box_height = min(height - 6, len(lines) + 4)

        start_y = (height - box_height) // 2
        start_x = (width - box_width) // 2

        # Luo ikkuna
        win = curses.newwin(box_height, box_width, start_y, start_x)
        win.box()

        # Otsikko
        win.attron(curses.color_pair(1) | curses.A_BOLD)
        win.addstr(0, 2, f" {title} ")
        win.attroff(curses.color_pair(1) | curses.A_BOLD)

        # Sisältö
        for idx, line in enumerate(lines[:box_height-4]):
            y = 2 + idx
            x = 2
            # Leikkaa liian pitkät rivit
            if len(line) > box_width - 4:
                line = line[:box_width-7] + "..."
            win.addstr(y, x, line)

        # Ohje
        footer = "Paina mitä tahansa näppäintä..."
        x = (box_width - len(footer)) // 2
        win.attron(curses.color_pair(2))
        win.addstr(box_height - 1, x, footer)
        win.attroff(curses.color_pair(2))

        win.refresh()
        win.getch()

        # Piirrä koko ruutu uudelleen
        self.draw_screen(stdscr)

    def check_installation(self, stdscr):
        """Tarkista asennus"""
        self.add_status("Tarkistetaan asennusta...", "INFO")
        self.draw_screen(stdscr)

        import subprocess

        checks = []
        venv_exists = (self.BASE_DIR / "venv").exists()
        piper_exists = (self.BASE_DIR / "piper" / "piper").exists()
        model_exists = (self.BASE_DIR / "fi_FI-asmo-medium.onnx").exists()

        checks.append(f"{'✓' if venv_exists else '✗'} Virtuaaliympäristö")
        checks.append(f"{'✓' if piper_exists else '✗'} Piper TTS")
        checks.append(f"{'✓' if model_exists else '✗'} Suomenkielinen äänimalli")

        if venv_exists and piper_exists and model_exists:
            checks.append("")
            checks.append("✅ Kaikki asennettu!")
            self.add_status("Asennus OK", "SUCCESS")
        else:
            checks.append("")
            checks.append("⚠️  Puuttuvia komponentteja")
            checks.append("Valitse 'Käynnistä' asentaaksesi")
            self.add_status("Puuttuvia komponentteja", "WARNING")

        self.show_message_box(stdscr, "Asennuksen tila", "", checks)

    def run_tests(self, stdscr):
        """Aja testit"""
        import subprocess

        self.add_status("Käynnistetään testit...", "INFO")
        self.draw_screen(stdscr)

        # Palautetaan normaali terminaali-tila
        curses.endwin()

        try:
            # Aja testit
            result = subprocess.run(
                [sys.executable, str(self.BASE_DIR / "scripts" / "aja_testit.py")],
                cwd=str(self.BASE_DIR)
            )

            # Palauta curses-tila
            stdscr.refresh()

            if result.returncode == 0:
                self.add_status("Testit suoritettu onnistuneesti", "SUCCESS")
            else:
                self.add_status(f"Testit epäonnistuivat: {result.returncode}", "ERROR")

        except Exception as e:
            # Palauta curses-tila virhetilanteessa
            stdscr.refresh()
            self.add_status(f"Virhe testien ajossa: {e}", "ERROR")

        self.draw_screen(stdscr)

    def show_help(self, stdscr):
        """Näytä ohjeet"""
        help_text = [
            "UUTISTENLUKIJA - KÄYTTÖOHJEET",
            "",
            "1. Käynnistä uutislukija",
            "   - Asentaa automaattisesti puuttuvat komponentit",
            "   - Lukee tämän päivän uutiset",
            "   - Vahtii uusia uutisia",
            "",
            "2. Tarkista asennus",
            "   - Näyttää mitä on asennettu",
            "",
            "3. Aja testit",
            "   - Testaa että kaikki toimii",
            "",
            "NAVIGOINTI:",
            "  ↑↓   - Liiku valikossa",
            "  ENTER - Valitse",
            "  Q     - Lopeta",
            "",
            "Projekti: github.com/...",
        ]

        self.show_message_box(stdscr, "Ohjeet", "", help_text)

    def start_reader(self, stdscr):
        """Käynnistä uutislukija"""
        import subprocess

        self.add_status("Käynnistetään lukijaa...", "INFO")
        self.draw_screen(stdscr)

        # Palautetaan normaali terminaali-tila
        curses.endwin()

        try:
            # Käynnistä kaynnista.py
            result = subprocess.run(
                [sys.executable, str(self.BASE_DIR / "kaynnista.py")],
                cwd=str(self.BASE_DIR)
            )

            # Palauta curses-tila
            stdscr.refresh()

            if result.returncode == 0:
                self.add_status("Lukija suoritettu onnistuneesti", "SUCCESS")
            else:
                self.add_status(f"Lukija palautti virheellä: {result.returncode}", "ERROR")

        except Exception as e:
            # Palauta curses-tila virhetilanteessa
            stdscr.refresh()
            self.add_status(f"Virhe käynnistyksessä: {e}", "ERROR")

        self.draw_screen(stdscr)

    def handle_menu_selection(self, stdscr):
        """Käsittele valikon valinta"""
        if self.current_menu == 0:  # Käynnistä
            self.start_reader(stdscr)
        elif self.current_menu == 1:  # Tarkista asennus
            self.check_installation(stdscr)
        elif self.current_menu == 2:  # Testit
            self.run_tests(stdscr)
        elif self.current_menu == 3:  # Ohjeet
            self.show_help(stdscr)
        elif self.current_menu == 4:  # Lopeta
            return False
        return True

    def main_loop(self, stdscr):
        """Pääsilmukka"""
        # Alusta värit
        curses.start_color()
        curses.use_default_colors()

        # Määrittele väriparit
        curses.init_pair(1, curses.COLOR_CYAN, -1)     # Otsikko
        curses.init_pair(2, curses.COLOR_WHITE, -1)    # Normaali teksti
        curses.init_pair(3, curses.COLOR_YELLOW, -1)   # Väliotsikot
        curses.init_pair(4, curses.COLOR_GREEN, -1)    # Valinta/Success
        curses.init_pair(5, curses.COLOR_RED, -1)      # Error
        curses.init_pair(6, curses.COLOR_YELLOW, -1)   # Warning

        # Piilota kursori
        curses.curs_set(0)

        # Aseta näppäinten timeout
        stdscr.timeout(100)  # 100ms timeout

        self.add_status("Tervetuloa Uutistenlukijaan!", "INFO")
        self.add_status("Käytä nuolinäppäimiä navigointiin", "INFO")

        running = True
        while running:
            # Piirrä näyttö
            self.draw_screen(stdscr)

            # Lue näppäin
            try:
                key = stdscr.getch()

                if key == curses.KEY_UP:
                    self.current_menu = (self.current_menu - 1) % len(self.menu_items)
                elif key == curses.KEY_DOWN:
                    self.current_menu = (self.current_menu + 1) % len(self.menu_items)
                elif key in [curses.KEY_ENTER, ord('\n'), ord('\r')]:
                    running = self.handle_menu_selection(stdscr)
                elif key in [ord('q'), ord('Q')]:
                    running = False

            except KeyboardInterrupt:
                running = False

    def run(self):
        """Käynnistä TUI"""
        try:
            curses.wrapper(self.main_loop)
        except Exception as e:
            print(f"{SimpleColors.RED}Virhe TUI:ssa: {e}{SimpleColors.END}")
            print(f"{SimpleColors.YELLOW}Varmista että terminaali tukee curses:ia{SimpleColors.END}")
            sys.exit(1)

def main():
    """Pääohjelma"""
    tui = UutislukijaTUI()
    tui.run()

if __name__ == "__main__":
    main()
