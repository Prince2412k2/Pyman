import curses
import logging
import time

logging.basicConfig(filename="debug.log", level=logging.INFO)


class BaseWindow:
    def __init__(self, height, width, y, x) -> None:
        self.win = curses.newwin(height, width, y, x)

    def resize(self, y_len, x_len):
        self.win.resize(y_len, x_len)

    def move(self, y, x):
        self.win.move(y, x)

    def erase(self):
        self.win.erase()

    def draw_border(self):
        self.win.box()

    def refresh(self):
        self.win.noutrefresh()


class MainWindow(BaseWindow):
    def draw(self):
        self.erase()
        self.win.addstr(2, 2, "helloworld")


class OptionsWindow(BaseWindow):
    def draw(self):
        self.erase()
        self.win.addstr(2, 2, "helloworld")


def main(stdscr):
    height, width = stdscr.getmaxyx()
    curses.curs_set(0)
    stdscr.nodelay(False)
    stdscr.keypad(True)

    curses.start_color()
    curses.use_default_colors()
    main_win = MainWindow(height - 4, width - 4, 2, 2)
    opt_win = OptionsWindow(height - 6, (width - 6) // 3, 5, 5)
    while True:
        stdscr.clear()
        while True:
            max_y, max_x = stdscr.getmaxyx()

            main_win.resize(max_y - 4, max_x - 4)
            opt_win.resize(height - 10, (width - 6) // 3)

            main_win.draw()
            opt_win.draw()

            main_win.draw_border()
            opt_win.draw_border()

            main_win.refresh()
            opt_win.refresh()
            curses.doupdate()

            win_key = main_win.win.getch()
            if win_key == ord("q"):
                break

        key = stdscr.getch()
        if key == ord("q"):
            break
        stdscr.refresh()


if __name__ == "__main__":
    curses.wrapper(main)
