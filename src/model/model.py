import random

SHAPES = {
    'I': [[1, 1, 1, 1]],
    'O': [[1, 1], [1, 1]],
    'T': [[0, 1, 0], [1, 1, 1]],
    'S': [[0, 1, 1], [1, 1, 0]],
    'Z': [[1, 1, 0], [0, 1, 1]],
    'J': [[1, 0, 0], [1, 1, 1]],
    'L': [[0, 0, 1], [1, 1, 1]]
}

class TetrisModel:
    def __init__(self, rows=20, columns=10):
        self.rows = rows
        self.columns = columns
        self.board = [[0] * columns for _ in range(rows)]
        self.piece = None
        self.is_game_over = False
        self.score = 0
        self.new_piece()

    def new_piece(self):
        shape = random.choice(list(SHAPES.keys()))
        self.piece = {
            'x': self.columns // 2 - 1,
            'y': 0,
            'shape': SHAPES[shape],
            'name': shape
        }
        if self.check_collision():
            self.is_game_over = True

    def move_piece(self, dx, dy):
        if self.piece and not self.is_game_over:
            old_x, old_y = self.piece['x'], self.piece['y']
            self.piece['x'] += dx
            self.piece['y'] += dy

            if self.check_collision():
                self.piece['x'], self.piece['y'] = old_x, old_y
                if dy == 1:
                    self.lock_piece()
                    self.piece = None
                    return False
            return True
        return False

    def rotate_piece(self):
        if self.piece:
            original_shape = self.piece['shape']
            self.piece['shape'] = [list(row) for row in zip(*self.piece['shape'][::-1])]
            if self.check_collision():
                self.piece['shape'] = original_shape

    def check_collision(self, blocked_only=False):
        if not self.piece:
            return False
            
        shape = self.piece['shape']
        for row_idx, row in enumerate(shape):
            for col_idx, cell in enumerate(row):
                if cell:
                    x = self.piece['x'] + col_idx
                    y = self.piece['y'] + row_idx
                    if x < 0 or x >= self.columns or y >= self.rows:
                        return True
                    if y >= 0 and self.board[y][x]:
                        return True if not blocked_only else (y > 0)
        return False

    def lock_piece(self):
        if self.piece:
            shape = self.piece['shape']
            for row_idx, row in enumerate(shape):
                for col_idx, cell in enumerate(row):
                    if cell:
                        x = self.piece['x'] + col_idx
                        y = self.piece['y'] + row_idx
                        if y >= 0:
                            self.board[y][x] = 1
            self.clear_lines()

    def clear_lines(self):
        new_board = [row for row in self.board if any(cell == 0 for cell in row)]
        lines_cleared = self.rows - len(new_board)
        self.board = [[0] * self.columns for _ in range(lines_cleared)] + new_board
        self.score += lines_cleared * 100
