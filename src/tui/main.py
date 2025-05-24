import curses
import logging
from pathlib import Path
import time
from src.tui.schema import Mapper
from src.core.config_handler import get_config
from src.core.env_handler import set_packages, get_paths
from src.tui.base import Menu

logger = logging.getLogger(__name__)
mapper = Mapper()


def config_window(win, key, height, width):
    if key != ord("?"):
        return
    while True:
        new_height = max(5, height - 4)
        new_width = max(5, width // 2 - 1)
        win.resize(new_height, new_width)
        win.mvwin(2, new_width + 2)
        win.erase()
        win.addstr(1, 1, "helo")
        win.box()
        win.refresh()
        win_key = win.getch()
        if win_key == ord("c"):
            win.clear()
            break


def print_items(win, menu: Menu):
    for idx, i in enumerate(menu.items):
        color = curses.A_STANDOUT if idx == menu.selected else curses.A_NORMAL
        win.addstr(idx + menu.margin + 1, 3, str(i.parent.name), color)


class ScrollableMenu:
    def __init__(self, items, height, width, begin_y, begin_x):
        self.items = items
        self.window = curses.newwin(height, width, begin_y, begin_x)
        self.height = height - 2  # inner height after box
        self.width = width
        self.selected = 0
        self.offset = 0
        self.focus = True

    def draw(self, re_y, re_x, mv_y, mv_x, name):
        self.height = re_y - 2
        self.width = re_x
        self.window.resize(re_y, re_x)
        self.window.mvwin(mv_y, mv_x)
        self.window.erase()

        color = curses.color_pair(4) if self.focus else curses.A_NORMAL
        self.window.attron(color)
        self.window.box()
        self.window.attroff(color)

        max_visible = self.height - 1
        visible_items = self.items[self.offset : self.offset + max_visible]
        self.window.addstr(0, 1, name, curses.color_pair(3))
        for idx, item in enumerate(visible_items):
            env_meta = mapper.get(item)
            y = idx + 2
            attr = (
                curses.A_REVERSE
                if (self.offset + idx) == self.selected
                else curses.A_NORMAL
            )
            self.window.addstr(y, 2, env_meta.icon, curses.color_pair(env_meta.color))
            self.window.addnstr(y, 4, f"{item.get_name()}", self.width - 2, attr)

        self.window.noutrefresh()
        logger.info(self.items[self.selected])
        return self.items[self.selected]

    def handle_key(self, key):
        if key == curses.KEY_DOWN:
            if self.selected > len(self.items) - 2:
                self.offset = 0
                self.selected = 0
                return
            self.selected += 1
            if self.selected >= self.offset + self.height:
                self.offset += 1

        elif key == curses.KEY_UP:
            if self.selected < 1:
                if len(self.items) > self.height:
                    self.offset = len(self.items) % self.height
                self.selected = len(self.items) - 1
                return
            self.selected -= 1
            if self.selected < self.offset:
                self.offset -= 1
        elif key == ord("r"):
            conf = get_config()
            assert conf
            self.items = get_paths(conf).get_all()
        logger.info(f"offset {self.offset}")
        logger.info(f"selected {self.selected}")


def initcolor():
    curses.initscr()
    curses.start_color()
    curses.init_pair(1, curses.COLOR_YELLOW, -1)
    curses.init_pair(2, 120, -1)
    curses.init_pair(3, curses.COLOR_CYAN, -1)
    curses.init_pair(4, 117, -1)


def main(stdscr):
    y, x = stdscr.getmaxyx()
    curses.curs_set(0)
    stdscr.nodelay(False)
    stdscr.keypad(True)

    curses.use_default_colors()
    conf = get_config()
    assert conf
    envs = get_paths(conf)

    initcolor()
    env_menu = ScrollableMenu(
        envs.get_all(), height=y // 2, width=x // 3, begin_y=0, begin_x=0
    )
    package_menu = ScrollableMenu(
        envs.get_all()[0].packages,
        height=y // 2 - 2,
        width=x // 3,
        begin_y=y // 2 + 1,
        begin_x=0,
    )

    while True:
        y, x = stdscr.getmaxyx()
        env = env_menu.draw(y // 2, x // 3, 0, 0, "Envs")
        env = set_packages(env)
        assert env
        package_menu.items = env.packages
        package_menu.draw(y // 2 - 2, x // 3, y // 2 + 1, 0, "Pkgs")
        curses.doupdate()
        key = stdscr.getch()
        if key in [ord("q"), 27]:
            break
        env_menu.handle_key(key)


if __name__ == "__main__":
    curses.wrapper(main)
