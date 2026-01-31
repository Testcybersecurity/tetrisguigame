import tkinter as tk
import random

# =========================
# TETRIS GAME
# =========================
class Tetris:
    def __init__(self, root):
        self.root = root
        self.root.title("Tetris")
        self.root.resizable(False, False)

        self.cell_size = 30
        self.cols = 10
        self.rows = 20

        self.score = 0
        self.level = 1
        self.speed = 500

        self.colors = ["cyan", "blue", "orange", "yellow", "green", "purple", "red"]

        self.shapes = [
            [[1, 1, 1, 1]],                    # I
            [[1, 1, 1], [0, 1, 0]],           # T
            [[1, 1, 1], [1, 0, 0]],           # L
            [[1, 1, 1], [0, 0, 1]],           # J
            [[1, 1], [1, 1]],                # O
            [[0, 1, 1], [1, 1, 0]],           # S
            [[1, 1, 0], [0, 1, 1]]            # Z
        ]

        self.build_ui()
        self.bind_keys()

        self.reset_board()
        self.new_piece()
        self.update()

    # =========================
    # UI
    # =========================
    def build_ui(self):
        frame = tk.Frame(self.root)
        frame.pack()

        self.canvas = tk.Canvas(
            frame,
            width=self.cols * self.cell_size,
            height=self.rows * self.cell_size,
            bg="black"
        )
        self.canvas.grid(row=0, column=0, rowspan=4)

        self.score_label = tk.Label(frame, text="Score: 0", font=("Segoe UI", 14))
        self.score_label.grid(row=0, column=1, padx=10, pady=5)

        self.level_label = tk.Label(frame, text="Level: 1", font=("Segoe UI", 14))
        self.level_label.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(frame, text="Controls:\n← → Move\n↑ Rotate\n↓ Drop\nR Restart",
                 font=("Segoe UI", 10)).grid(row=2, column=1, padx=10, pady=10)

    # =========================
    # GAME LOGIC
    # =========================
    def reset_board(self):
        self.board = [[None for _ in range(self.cols)] for _ in range(self.rows)]

    def new_piece(self):
        self.shape = random.choice(self.shapes)
        self.color = random.choice(self.colors)
        self.x = self.cols // 2 - len(self.shape[0]) // 2
        self.y = 0

        if self.check_collision(self.x, self.y, self.shape):
            self.game_over()

    def rotate(self):
        rotated = list(zip(*self.shape[::-1]))
        rotated = [list(row) for row in rotated]

        if not self.check_collision(self.x, self.y, rotated):
            self.shape = rotated

    def check_collision(self, x, y, shape):
        for r, row in enumerate(shape):
            for c, cell in enumerate(row):
                if cell:
                    nx = x + c
                    ny = y + r

                    if nx < 0 or nx >= self.cols or ny >= self.rows:
                        return True
                    if ny >= 0 and self.board[ny][nx]:
                        return True
        return False

    def freeze_piece(self):
        for r, row in enumerate(self.shape):
            for c, cell in enumerate(row):
                if cell:
                    self.board[self.y + r][self.x + c] = self.color

        self.clear_lines()
        self.new_piece()

    def clear_lines(self):
        full_rows = [i for i, row in enumerate(self.board) if all(row)]
        for row in full_rows:
            del self.board[row]
            self.board.insert(0, [None for _ in range(self.cols)])

        if full_rows:
            self.score += len(full_rows) * 100
            self.level = self.score // 500 + 1
            self.speed = max(100, 500 - (self.level - 1) * 40)

            self.score_label.config(text=f"Score: {self.score}")
            self.level_label.config(text=f"Level: {self.level}")

    # =========================
    # MOVEMENT
    # =========================
    def move(self, dx, dy):
        if not self.check_collision(self.x + dx, self.y + dy, self.shape):
            self.x += dx
            self.y += dy
        elif dy == 1:
            self.freeze_piece()

    def drop(self):
        while not self.check_collision(self.x, self.y + 1, self.shape):
            self.y += 1
        self.freeze_piece()

    # =========================
    # DRAWING
    # =========================
    def draw(self):
        self.canvas.delete("all")

        for r in range(self.rows):
            for c in range(self.cols):
                if self.board[r][c]:
                    self.draw_cell(c, r, self.board[r][c])

        for r, row in enumerate(self.shape):
            for c, cell in enumerate(row):
                if cell:
                    self.draw_cell(self.x + c, self.y + r, self.color)

    def draw_cell(self, x, y, color):
        px = x * self.cell_size
        py = y * self.cell_size
        self.canvas.create_rectangle(
            px, py, px + self.cell_size, py + self.cell_size,
            fill=color, outline="gray"
        )

    # =========================
    # LOOP
    # =========================
    def update(self):
        self.move(0, 1)
        self.draw()
        self.root.after(self.speed, self.update)

    # =========================
    # INPUT
    # =========================
    def bind_keys(self):
        self.root.bind("<Left>", lambda e: self.move(-1, 0))
        self.root.bind("<Right>", lambda e: self.move(1, 0))
        self.root.bind("<Down>", lambda e: self.move(0, 1))
        self.root.bind("<Up>", lambda e: self.rotate())
        self.root.bind("r", lambda e: self.restart())

    # =========================
    # GAME OVER / RESTART
    # =========================
    def game_over(self):
        self.canvas.create_text(
            self.cols * self.cell_size // 2,
            self.rows * self.cell_size // 2,
            text="GAME OVER\nPress R to Restart",
            fill="white",
            font=("Segoe UI", 24)
        )
        self.root.after_cancel(self.update)

    def restart(self):
        self.score = 0
        self.level = 1
        self.speed = 500
        self.score_label.config(text="Score: 0")
        self.level_label.config(text="Level: 1")
        self.reset_board()
        self.new_piece()


# =========================
# RUN
# =========================
if __name__ == "__main__":
    root = tk.Tk()
    game = Tetris(root)
    root.mainloop()
