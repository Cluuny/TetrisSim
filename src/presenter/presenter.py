import pygame
import time

class TetrisPresenter:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.running = True
        self.paused = False
        self.last_fall_time = time.time()
        self.fall_delay = 0.5
        self.last_down_press = 0
        self.last_rotate_press = 0
        self.input_delay = 0.15

    def run(self):
        while self.running:
            self.running = self.view.handle_events()

            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                self.paused = not self.paused
                time.sleep(0.2)

            if not self.model.is_game_over and not self.paused:
                current_time = time.time()

                if self.model.piece is None:
                    self.model.new_piece()

                elif current_time - self.last_fall_time >= self.fall_delay:
                    if not self.model.move_piece(0, 1):
                        self.model.lock_piece()
                        self.model.new_piece()
                    self.last_fall_time = current_time

                self.handle_input(current_time)

            self.view.render(paused=self.paused)
            pygame.time.delay(20)

    def handle_input(self, current_time):
        if not self.paused:
            keys = pygame.key.get_pressed()
            
            if keys[pygame.K_LEFT]:
                self.model.move_piece(-1, 0)
                pygame.time.delay(50)
            elif keys[pygame.K_RIGHT]:
                self.model.move_piece(1, 0)
                pygame.time.delay(50)

            if keys[pygame.K_DOWN]:
                if current_time - self.last_down_press > self.input_delay:
                    while self.model.piece and not self.model.check_collision():
                        self.model.move_piece(0, 1)
                    self.model.lock_piece()
                    self.last_down_press = current_time

            if keys[pygame.K_UP]:
                if current_time - self.last_rotate_press > self.input_delay:
                    self.model.rotate_piece()
                    self.last_rotate_press = current_time
