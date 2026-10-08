import pygame
from .snake import Snake
from .food import Food

# Game Engine

WHITE = (255, 255, 255)
GREEN = (0, 200, 0)
RED = (220, 60, 60)
GRAY = (180, 180, 180)

class GameEngine:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.cell_size = 20
        self.grid_width = width // self.cell_size
        self.grid_height = height // self.cell_size

        self.snake = Snake(self.grid_width // 2, self.grid_height // 2, self.cell_size)
        self.food = Food(self.grid_width, self.grid_height, self.cell_size)
        # Make sure the first food never spawns on top of the snake.
        self.food.respawn(self.snake.body)

        self.score = 0
        self.font = pygame.font.SysFont("Arial", 30)
        self.big_font = pygame.font.SysFont("Arial", 64, bold=True)
        self.small_font = pygame.font.SysFont("Arial", 26)

        self.moves_per_second = 8
        self._frame_counter = 0

        self.game_over = False
        self.game_over_time = 0

    def _end_game(self):
        self.game_over = True
        self.game_over_time = pygame.time.get_ticks()

    def handle_keydown(self, key):
        if self.game_over:
            # Short delay so a key pressed just before dying doesn't skip the screen.
            if pygame.time.get_ticks() - self.game_over_time > 700:
                pygame.event.post(pygame.event.Event(pygame.QUIT))
            return

        if key in (pygame.K_UP, pygame.K_w):
            self.snake.set_direction(0, -1)
        elif key in (pygame.K_DOWN, pygame.K_s):
            self.snake.set_direction(0, 1)
        elif key in (pygame.K_LEFT, pygame.K_a):
            self.snake.set_direction(-1, 0)
        elif key in (pygame.K_RIGHT, pygame.K_d):
            self.snake.set_direction(1, 0)

    def handle_input(self):
        # Reserved for continuously-held-key input (not used for a
        # grid-based snake, but kept here to mirror the engine's shape).
        pass

    def update(self):
        if self.game_over:
            return

        self._frame_counter += 1
        frames_per_move = max(1, 60 // self.moves_per_second)
        if self._frame_counter < frames_per_move:
            return
        self._frame_counter = 0

        self.snake.move()

        if self.snake.collides_with_wall(self.grid_width, self.grid_height):
            self._end_game()
            return

        if self.snake.collides_with_self():
            self._end_game()
            return

        if self.snake.head_rect().colliderect(self.food.rect()):
            self.snake.grow()
            self.score += 1
            self.food.respawn(self.snake.body)

    def _draw_text(self, screen, text, font, color, y):
        surface = font.render(text, True, color)
        rect = surface.get_rect(center=(self.width // 2, y))
        screen.blit(surface, rect)

    def _draw_game_over(self, screen):
        overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))

        self._draw_text(screen, "GAME OVER", self.big_font, RED, self.height // 2 - 70)
        self._draw_text(screen, f"Final Score: {self.score}", self.font, WHITE, self.height // 2)
        self._draw_text(screen, "Press any key to exit", self.small_font, GRAY, self.height // 2 + 60)

    def render(self, screen):
        # Draw food
        pygame.draw.rect(screen, RED, self.food.rect())

        # Draw snake
        for rect in self.snake.segment_rects():
            pygame.draw.rect(screen, GREEN, rect)

        # Draw score
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        if self.game_over:
            self._draw_game_over(screen)