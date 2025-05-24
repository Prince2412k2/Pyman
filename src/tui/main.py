import curses
import logging
from pathlib import Path
from src.tui.schema import Mapper, State, WindowTypes
from src.core.config_handler import get_config
from src.core.env_handler import set_packages, get_paths

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


class ScrollableMenu:
    def __init__(self, items, height, width, begin_y, begin_x, selected=0, focus=True):
        self.items = items
        self.window = curses.newwin(height, width, begin_y, begin_x)
        self.height = height - 2  # inner height after box
        self.width = width
        self.selected = selected
        self.offset = 0
        self.focus = focus

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

        max_visible = self.height
        visible_items = self.items[self.offset : self.offset + max_visible]
        self.window.addstr(0, 1, name, curses.color_pair(3))
        for idx, item in enumerate(visible_items):
            env_meta = mapper.get(item)
            y = idx + 1
            attr = (
                curses.A_REVERSE
                if (self.offset + idx) == self.selected
                else curses.A_NORMAL
            )
            if env_meta.icon:
                self.window.addstr(
                    y, 2, env_meta.icon, curses.color_pair(env_meta.color)
                )
            self.window.addnstr(y, 4, f"{item.get_name()}", self.width - 2, attr)

        self.window.noutrefresh()
        return self.items[self.selected]

    def handle_key(self, key, state):
        if key == curses.KEY_DOWN:
            if self.selected > len(self.items) - 2:
                self.offset = 0
                self.selected = 0
                return
            self.selected += 1
            if self.selected >= self.offset + self.height:
                self.offset += 1
            logger.info(f"{self.selected} ")
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
        elif key == ord("o"):
            self.focus = False
            self.selected, self.offset = (
                (-1, 0)
                if state.focus == WindowTypes.PACKAGE
                else (self.selected, self.offset)
            )
            state.focus = (
                WindowTypes.ENV
                if state.focus == WindowTypes.PACKAGE
                else WindowTypes.PACKAGE
            )
            logger.info(state.focus)


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
        height=y // 2 - 3,
        width=x // 3,
        begin_y=y // 2,
        begin_x=0,
        selected=-1,
        focus=False,
    )
    state = State(focus=WindowTypes.ENV)
    while True:
        y, x = stdscr.getmaxyx()

        if state.focus == WindowTypes.PACKAGE:
            package_menu.focus = True
        elif state.focus == WindowTypes.ENV:
            env_menu.focus = True

        env = env_menu.draw(y // 2, x // 3, 0, 0, "Envs")
        env = set_packages(env)
        assert env
        package_menu.items = env.packages

        package_menu.draw(y // 2 - 1, x // 3, y // 2 + 1, 0, "Pkgs")
        curses.doupdate()
        key = stdscr.getch()
        if key in [ord("q"), 27]:
            break
        if state.focus == WindowTypes.PACKAGE:
            package_menu.handle_key(key, state)
        else:
            env_menu.handle_key(key, state)


if __name__ == "__main__":
    curses.wrapper(main)
