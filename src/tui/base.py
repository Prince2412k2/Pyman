from pathlib import Path
from typing import List


class Menu:
    def __init__(self, items: List[Path], margin=1) -> None:
        self.items = items
        self.selected: int = 0
        self.margin: int = margin

    def up(self):
        self.selected = self.selected - 1 if self.selected > 0 else len(self.items) - 1

    def down(self):
        self.selected = self.selected + 1 if self.selected < len(self.items) - 1 else 0
