import curses
import time
from typing import List
from pathlib import Path


def print_v(items, pad: curses.window, selected):
    for idx, i in enumerate(items):
        color = curses.A_STANDOUT if idx == selected else curses.A_NORMAL
        pad.addstr(idx, 1, i, color)


def list_view(stdscr, items, y, x):
    win = curses.newwin(y - 1, x // 2, 0, 0)
    pad = curses.newpad(len(items), x // 2)
    scroll = 0
    selected = 0
    while True:
        win.resize(y - 1, x // 2)
        win.move(0, 0)
        win.erase()
        win.box()
        win.noutrefresh()
        pad.erase()
        print_v(items, pad, selected)
        pad.noutrefresh(scroll, 1, 1, 1, y - 4, x // 2 - 2)
        curses.doupdate()
        win_key = stdscr.getch()
        if win_key == ord("q"):
            win.clear()
            pad.clear()
            break
        if win_key == curses.KEY_DOWN:
            selected = selected + 1 if selected < y - 4 else 0
            scroll = scroll + 1 if selected == y - 6 else scroll
        if win_key == curses.KEY_UP:
            selected = selected - 1 if selected > 0 else len(items) - 4
            scroll = scroll - 1 if selected == 6 else scroll


class Menu:
    def __init__(self, items, y, x) -> None:
        """y,x are supposed to be in compared to max_x max_y"""
        self.items: List[Path] = items
        self.pad_len = len(items)
        self.selected = 0
        self.start_at = 0
        self.cols = x
        self.lines = y
        self.init()

    def init(self):
        self.window = curses.newwin(2, 2, 0, 0)
        self.pad = curses.newpad(self.pad_len, self.cols)

    def down(self):
        if self.selected > self.pad_len - 4 and self.start_at < self.pad_len - 1:
            self.start_at += 1
        self.selected = (
            self.selected + 1 if self.selected < self.pad_len - 1 else self.selected
        )

    def up(self):
        if self.selected < 3 and self.start_at > 0:
            self.start_at -= 1
        self.selected = self.selected - 1 if self.selected > 0 else self.selected

    def adjust(self, ry, rx, my, mx):
        """ry : nlines for resize
        rx : ncols for resize
        my : y cordinate for move
        mx : x cordinate for move
        """
        self.cols, self.lines = rx, ry

        self.window.resize(ry, rx)
        self.window.mvwin(my, mx)

        self.wy, self.wx = self.window.getbegyx()

        self.window.erase()
        self.pad.erase()

        self.print_items()

        self.window.box()
        self.pad.noutrefresh(
            self.start_at,
            0,
            self.wy + 1,
            self.wx + 1,
            self.wy + ry - 2,
            self.wx + rx - 2,
        )
        self.window.noutrefresh()
        curses.doupdate()

    def print_items(self):
        for idx, i in enumerate(self.items):
            color = curses.A_STANDOUT if idx == self.selected else curses.A_NORMAL
            self.pad.addstr(idx, 0, str(i), color)


def menup(stdscr, menu: Menu):
    y, x = stdscr.getmaxyx()
    while True:
        menu.adjust(y - 2, x // 2, 0, 0)
        key = stdscr.getch()
        if key == curses.KEY_UP:
            menu.up()
        if key == curses.KEY_DOWN:
            menu.down()

        if key == ord("q"):
            break


def main(stdscr):
    y, x = stdscr.getmaxyx()
    curses.curs_set(0)
    stdscr.nodelay(False)
    stdscr.keypad(True)

    curses.start_color()
    curses.use_default_colors()

    it = [f"item-{i}" for i in range(100)]
    menu = Menu(it, y, x)

    while True:
        stdscr.erase()
        stdscr.refresh()
        menup(stdscr, menu)
        key = stdscr.getch()
        if key == ord("q"):
            break
        time.sleep(0.5)
