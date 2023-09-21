# tetris_mvp/view.py
import pygame

class TetrisView:
    def __init__(self, model):
        pygame.init()
        self.model = model
        self.cell_size = 30
        self.board_width = model.columns * self.cell_size
        self.board_height = model.rows * self.cell_size
        self.panel_height = 50
        self.screen = pygame.display.set_mode((self.board_width, self.board_height + self.panel_height))
        pygame.display.set_caption("Tetris Sim")
        self.font = pygame.font.Font(None, 36)

        self.colors = {
            'I': (0, 255, 255),
            'O': (255, 255, 0),
            'T': (128, 0, 128),
            'S': (0, 255, 0),
            'Z': (255, 0, 0),
            'J': (0, 0, 255),
            'L': (255, 165, 0),
            'default': (0, 0, 0)
        }

    def render(self, paused=False):
        self.screen.fill((255, 255, 255))

        for y, row in enumerate(self.model.board):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(
                        self.screen,
                        self.colors['default'],
                        (x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size)
                    )

        if self.model.piece and not self.model.is_game_over:
            shape = self.model.piece['shape']
            color = self.colors.get(self.model.piece['name'], self.colors['default'])
            for row_idx, row in enumerate(shape):
                for col_idx, cell in enumerate(row):
                    if cell:
                        x = self.model.piece['x'] + col_idx
                        y = self.model.piece['y'] + row_idx
                        pygame.draw.rect(
                            self.screen,
                            color,
                            (x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size)
                        )

        pygame.draw.rect(
            self.screen,
            (0, 0, 0),
            (0, self.board_height, self.board_width, self.panel_height)
        )
        
        score_text = self.font.render(f"Puntuación: {self.model.score}", True, (255, 255, 255))
        self.screen.blit(score_text, (10, self.board_height + 10))

        if self.model.is_game_over:
            game_over_text = self.font.render("Juego Terminado", True, (255, 0, 0))
            self.screen.blit(game_over_text, (50, self.board_height // 2))

        if paused:
            pause_text = self.font.render("Juego en Pausa", True, (255, 0, 0))
            self.screen.blit(pause_text, (50, self.board_height // 2))

        pygame.display.flip()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
        return True

    def quit(self):
        pygame.quit()
