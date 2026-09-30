import random

# (rows, cols, mines) for each difficulty, kept in memory only
DIFFICULTIES = {
    "easy": (6, 6, 6),
    "medium": (9, 9, 12),
    "hard": (12, 12, 30),
}

DEFAULT_ROWS = 6
DEFAULT_COLS = 6
DEFAULT_MINES = 6


class Board:
    def __init__(self, rows=DEFAULT_ROWS, cols=DEFAULT_COLS, mines=DEFAULT_MINES):
        if mines >= rows * cols:
            raise ValueError("Too many mines for this board size.")
        self.rows = rows
        self.cols = cols
        self.mine_total = mines
        self.mines = self._build_mines()
        self.revealed = set()
        self.flags = set()

    def _build_mines(self):
        cells = [(r, c) for r in range(self.rows) for c in range(self.cols)]
        return set(random.sample(cells, self.mine_total))

    def in_bounds(self, r, c):
        return 0 <= r < self.rows and 0 <= c < self.cols

    def neighbors(self, r, c):
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                if dr == 0 and dc == 0:
                    continue
                nr, nc = r + dr, c + dc
                if self.in_bounds(nr, nc):  # FIX: was <= rows / <= cols
                    yield nr, nc

    def adjacent_mines(self, r, c):
        return sum(pos in self.mines for pos in self.neighbors(r, c))

    def reveal(self, start):
        """Reveal a cell (flood-filling zeros).
        Returns (hit_mine, newly_revealed_count)."""
        if start in self.flags or start in self.revealed:
            return False, 0
        if start in self.mines:
            return True, 0

        stack = [start]
        count = 0
        while stack:
            pos = stack.pop()
            if pos in self.revealed or pos in self.flags or pos in self.mines:
                continue
            self.revealed.add(pos)
            count += 1
            r, c = pos
            if self.adjacent_mines(r, c) == 0:
                stack.extend(n for n in self.neighbors(r, c)
                             if n not in self.revealed)
        return False, count

    def toggle_flag(self, pos):
        if pos in self.revealed:
            return False
        if pos in self.flags:
            self.flags.remove(pos)
        else:
            self.flags.add(pos)
        return True

    def won(self):
        # Win only when every non-mine cell has been revealed
        safe_cells = {(r, c) for r in range(self.rows) for c in range(self.cols)
                      if (r, c) not in self.mines}
        return safe_cells <= self.revealed
