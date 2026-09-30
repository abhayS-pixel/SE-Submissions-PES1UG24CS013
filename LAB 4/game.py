from board import Board, DIFFICULTIES


class Minesweeper:
    def __init__(self, difficulty="easy"):
        self.difficulty = difficulty
        self.board = Board(*DIFFICULTIES[difficulty])

    def choose_difficulty(self):
        aliases = {"e": "easy", "m": "medium", "h": "hard"}
        while True:
            raw = input("Choose difficulty (easy / medium / hard): ").strip().lower()
            raw = aliases.get(raw, raw)
            if raw in DIFFICULTIES:
                return raw
            print("Please type easy, medium or hard.")

    def display(self, reveal_mines=False):
        b = self.board
        w = len(str(max(b.rows, b.cols)))
        print("\n" + " " * (w + 1) + " ".join(f"{c + 1:>{w}}" for c in range(b.cols)))
        for r in range(b.rows):
            cells = []
            for c in range(b.cols):
                pos = (r, c)
                if reveal_mines and pos in b.mines:
                    ch = "*"
                elif pos in b.flags:
                    ch = "F"
                elif pos not in b.revealed:
                    ch = "#"
                else:
                    ch = str(b.adjacent_mines(r, c))
                cells.append(f"{ch:>{w}}")
            print(f"{r + 1:>{w}} " + " ".join(cells))

    def run(self):
        print("Minesweeper")
        self.difficulty = self.choose_difficulty()
        self.board = Board(*DIFFICULTIES[self.difficulty])
        print(f"Mode: {self.difficulty} "
              f"({self.board.rows}x{self.board.cols}, {self.board.mine_total} mines)")
        print("Commands: r row col | f row col | q")

        while True:
            self.display()
            print(f"Flags left: {self.board.mine_total - len(self.board.flags)}")
            raw = input("> ").strip().lower()
            if raw == "q":
                return
            parts = raw.split()
            if len(parts) != 3 or parts[0] not in {"r", "f"}:
                print("Use r row col or f row col.")
                continue
            try:
                r, c = int(parts[1]) - 1, int(parts[2]) - 1
            except ValueError:
                print("Coordinates must be numbers.")
                continue
            if not self.board.in_bounds(r, c):
                print("Outside the board.")
                continue

            pos = (r, c)

            if parts[0] == "f":
                if self.board.toggle_flag(pos):
                    state = "placed on" if pos in self.board.flags else "removed from"
                    print(f"Flag {state} ({r + 1}, {c + 1}).")
                else:
                    print("Can't flag a revealed cell.")
                continue

            # Reveal command
            if pos in self.board.flags:
                print("That cell is flagged. Remove the flag first.")
                continue
            if pos in self.board.revealed:
                print("That cell is already revealed.")
                continue

            hit_mine, count = self.board.reveal(pos)
            if hit_mine:
                self.display(reveal_mines=True)
                print("BOOM! You hit a mine.")
                return

            # One message per player action, not per flood-fill step
            if count == 1:
                print("Revealed 1 cell.")
            else:
                print(f"Opened an area: {count} cells revealed.")

            if self.board.won():
                self.display()
                print("You cleared the board! You win!")
                return
