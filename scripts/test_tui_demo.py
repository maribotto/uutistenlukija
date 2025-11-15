#!/usr/bin/env python3
"""
Demo TUI:sta - Testaa että curses toimii
"""

import curses
import time

def demo(stdscr):
    # Alusta värit
    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_CYAN, -1)
    curses.init_pair(2, curses.COLOR_GREEN, -1)
    curses.init_pair(3, curses.COLOR_YELLOW, -1)

    curses.curs_set(0)  # Piilota kursori
    stdscr.clear()

    height, width = stdscr.getmaxyx()

    # Otsikko
    title = "🗞️  UUTISTENLUKIJA TUI DEMO  🗞️"
    x = (width - len(title)) // 2
    stdscr.attron(curses.color_pair(1) | curses.A_BOLD)
    stdscr.addstr(2, x, title)
    stdscr.attroff(curses.color_pair(1) | curses.A_BOLD)

    # Teksti
    messages = [
        "✓ Curses toimii!",
        "✓ Värit toimivat!",
        "✓ TUI toimii!",
        "",
        "Paina mitä tahansa näppäintä lopettaaksesi..."
    ]

    for idx, msg in enumerate(messages):
        y = 5 + idx
        x = (width - len(msg)) // 2
        if "✓" in msg:
            stdscr.attron(curses.color_pair(2))
        else:
            stdscr.attron(curses.color_pair(3))
        stdscr.addstr(y, x, msg)
        stdscr.attroff(curses.color_pair(2))
        stdscr.attroff(curses.color_pair(3))

    stdscr.refresh()
    stdscr.getch()

if __name__ == "__main__":
    try:
        curses.wrapper(demo)
        print("\n✅ TUI-demo onnistui!")
    except Exception as e:
        print(f"\n❌ Virhe: {e}")
