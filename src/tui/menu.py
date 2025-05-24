import curses
from os import name
from time import sleep
from typing import List, Optional
from pathlib import Path
import logging
import locale

from src.core.schema import Kind

from src.core.env_handler import get_packages, get_paths
from src.core.schema import Env

from src.core.config_handler import get_config

locale.setlocale(locale.LC_ALL, "")
logger = logging.getLogger(__name__)


class EnvMenu:
    def __init__(self, items, height, width, y, x) -> None:
        """height  : num of lines
        width   : num of colmns
        y       : y cordinate of upper left corner
        x       : x cordinate of upper left corner
        """
        self.items: List[Env] = items
        self.pad_len = len(self.items)
        self.selected = 0
        self.start_at = 0
        self.init(height, width, y, x)

    def init(self, height, width, y_at, x_at):
        self.window = curses.newwin(height, width, y_at, x_at)
        self.pad = curses.newpad(self.pad_len, 100)

    def down(self, height):
        if (
            self.selected - self.start_at > height - 6
            # and self.selected + self.start_at < height - 2
            # and self.selected + self.start_at > height - 3
        ):
            self.start_at += 1

        if self.selected < self.pad_len - 1:
            self.selected = self.selected + 1
        else:
            self.selected = 0
            self.start_at = 0
        logger.info(f"sel:{self.selected}")
        logger.info(f"scroll:{self.start_at}")

    def up(self, height):
        if self.selected < self.start_at + 4 and self.start_at > 0:
            self.start_at -= 1

        if self.selected > 0:
            self.selected = self.selected - 1
        else:
            self.selected = self.pad_len - 1
            self.start_at = self.pad_len - height + 4
        logger.info(f"sel:{self.selected}")
        logger.info(f"scroll:{self.start_at}")

    def adjust(self, height, width, y, x, name):
        """height  : num of lines
        width   : num of colmns
        y       : y cordinate of upper left corner
        x       : x cordinate of upper left corner
        """

        self.window.resize(height, width)
        self.window.mvwin(y, x)

        self.window.erase()
        self.pad.clear()
        self.pad = curses.newpad(self.pad_len, 100)
        self.print_items()
        self.window.box()

        self.window.addstr(0, 2, name)

        self.window.noutrefresh()
        self.pad.noutrefresh(
            self.start_at,
            0,
            y + 2,
            x + 1,
            height + 2,
            width - 2,
        )
        curses.doupdate()

    def print_items(self):
        for idx, i in enumerate(self.items):
            if i.kind == Kind.CONDA:
                icon = " "
                name = str(i.path.name)
                color = curses.color_pair(2)
            else:
                icon = " "
                name = str(i.path.parent.name)
                color = curses.color_pair(1)

            if idx == self.selected:
                color |= curses.A_STANDOUT
            else:
                color |= curses.A_NORMAL
            self.pad.addstr(idx, 3, f" {icon} {name}", color)


class PackageMenu:
    def __init__(self, height, width, y, x) -> None:
        """height  : num of lines
        width   : num of colmns
        y       : y cordinate of upper left corner
        x       : x cordinate of upper left corner
        """
        self.items: Optional[list] = None
        self.pad_len: Optional[int] = None
        self.selected = 0
        self.start_at = 0
        self.init(height, width, y, x)

    def init(self, height, width, y_at, x_at):
        self.window = curses.newwin(height, width, y_at, x_at)
        self.pad = curses.newpad(100, 100)

    def down(self, height):
        if self.selected - self.start_at > height - 6:
            self.start_at += 1

        if self.selected < self.pad_len - 1:
            self.selected = self.selected + 1
        else:
            self.selected = 0
            self.start_at = 0
        logger.info(f"sel:{self.selected}")
        logger.info(f"scroll:{self.start_at}")

    def up(self, height):
        if self.selected < self.start_at + 4 and self.start_at > 0:
            self.start_at -= 1

        if self.selected > 0:
            self.selected = self.selected - 1
        else:
            self.selected = self.pad_len - 1
            self.start_at = self.pad_len - height + 4
        logger.info(f"sel:{self.selected}")
        logger.info(f"scroll:{self.start_at}")

    def adjust(self, items, height, width, y, x, name):
        """height  : num of lines
        width   : num of colmns
        y       : y cordinate of upper left corner
        x       : x cordinate of upper left corner
        """
        self.items = items
        self.pad_len = len(self.items)

        # height = min(self.pad_len, height)
        self.window.resize(height, width)
        self.window.mvwin(y, x)

        self.window.erase()
        self.pad = curses.newpad(self.pad_len, 50)
        self.print_items()
        self.window.box()

        self.window.addstr(0, 2, name)

        self.window.noutrefresh()
        logger.info(f"y={y} ,x= {x},he={height},wi={width}")
        self.pad.noutrefresh(
            self.start_at,
            0,
            y,
            x,
            height,
            width,
        )
        curses.doupdate()

    def print_items(self):
        for idx, i in enumerate(self.items):
            # if i.kind == Kind.CONDA:
            #     icon = " "
            #     name = str(i.path.name)
            #     color = curses.color_pair(2)
            # else:
            #     icon = " "
            #     name = str(i.path.parent.name)
            #     color = curses.color_pair(1)

            # if idx == self.selected:
            # color |= curses.A_STANDOUT
            # else:
            # color |= curses.A_NORMAL
            self.pad.addstr(idx, 3, f" {i.name}")


def show(menu: EnvMenu, stdscr, height, width, y, x, name):
    """height  : num of lines
    width   : num of colmns
    y       : y cordinate of upper left corner
    x       : x cordinate of upper left corner
    """
    y_max, x_max = stdscr.getmaxyx()
    pkg_menu = PackageMenu(y_max // 2 - 5, x_max // 3, y_max // 2 + 5, 2)

    while True:
        menu.adjust(height, width, y, x, name)
        env = get_packages(menu.items[menu.selected])
        assert env
        logger.info(f"{stdscr.getmaxyx()}")
        pkg_menu.adjust(env.packages, 20, x_max // 3, 16, 2, "packages")
        key = stdscr.getch()
        if key == curses.KEY_UP:
            menu.up(height)
        if key == curses.KEY_DOWN:
            menu.down(height)
        if key == ord("c"):
            return menu.items[menu.selected]
        if key == ord("r"):
            menu.items = get_paths(get_config()).get_all()
        if key == ord("q"):
            break


def initcolor():
    curses.initscr()
    curses.start_color()
    curses.init_pair(1, curses.COLOR_YELLOW, -1)
    # curses.init_pair(2, curses.COLOR_GREEN, -1)
    curses.init_pair(2, 46, -1)


def main(stdscr):
    y, x = stdscr.getmaxyx()
    curses.curs_set(0)
    stdscr.nodelay(False)
    stdscr.keypad(True)
    curses.use_default_colors()
    config = get_config()
    assert config
    items = get_paths(config)

    envs = items.get_all()
    env_menu = EnvMenu(envs, y // 2, x // 3, 5, 2)
    initcolor()
    while True:
        stdscr.refresh()
        y, x = stdscr.getmaxyx()
        stdscr.erase()
        selected = show(env_menu, stdscr, y // 2, x // 3, 5, 2, "envs")
        if selected:
            logger.info(selected)
            exit()
        key = stdscr.getch()
        if key == ord("q"):
            break
