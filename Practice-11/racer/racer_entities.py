import pygame
import random

# Constants for logic
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
ROAD_LEFT = 60
ROAD_RIGHT = 340

BLUE = (50, 100, 220)
BLACK = (0, 0, 0)
YELLOW = (255, 215, 0)
LINE_COLOR = (255, 255, 255)

# Global speeds (Enemy speed is now a base that can increase)
ENEMY_SPEED = 6 
COIN_SPEED = 5
ROAD_SPEED = 5

class PlayerCar:
    def __init__(self):
        self.width, self.height = 40, 70
        self.x = SCREEN_WIDTH // 2 - self.width // 2
        self.y = SCREEN_HEIGHT - 120
        self.speed = 5

    def draw(self, surface):
        pygame.draw.rect(surface, BLUE, (self.x, self.y, self.width, self.height), border_radius=6)
        pygame.draw.rect(surface, (150, 200, 255), (self.x + 6, self.y + 8, self.width - 12, 18), border_radius=3)
        pygame.draw.rect(surface, (150, 200, 255), (self.x + 6, self.y + 42, self.width - 12, 14), border_radius=3)
        for dx, dy in [(-6, 8), (self.width-4, 8), (-6, 44), (self.width-4, 44)]:
            pygame.draw.rect(surface, BLACK, (self.x + dx, self.y + dy, 10, 18), border_radius=3)

    def move(self, keys):
        if keys[pygame.K_LEFT] and self.x > ROAD_LEFT + 5: self.x -= self.speed
        if keys[pygame.K_RIGHT] and self.x + self.width < ROAD_RIGHT - 5: self.x += self.speed
        if keys[pygame.K_UP] and self.y > 0: self.y -= self.speed
        if keys[pygame.K_DOWN] and self.y + self.height < SCREEN_HEIGHT: self.y += self.speed

    def get_rect(self):
        return pygame.Rect(self.x + 4, self.y + 4, self.width - 8, self.height - 8)

class EnemyCar:
    COLORS = [(220, 50, 50), (50, 180, 50), (200, 150, 0), (180, 50, 180)]
    def __init__(self, current_speed):
        self.width, self.height = 40, 70
        self.x = random.choice([80, 160, 240])
        self.y = -self.height
        # Use the passed speed to allow enemies to get faster over time
        self.speed = current_speed + random.uniform(-1, 2)
        self.color = random.choice(self.COLORS)

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (self.x, self.y, self.width, self.height), border_radius=6)
        pygame.draw.rect(surface, (200, 230, 200), (self.x + 6, self.y + 8, self.width - 12, 18), border_radius=3)
        pygame.draw.rect(surface, (200, 230, 200), (self.x + 6, self.y + 42, self.width - 12, 14), border_radius=3)
        for dx, dy in [(-6, 8), (self.width-4, 8), (-6, 44), (self.width-4, 44)]:
            pygame.draw.rect(surface, BLACK, (self.x + dx, self.y + dy, 10, 18), border_radius=3)

    def update(self): self.y += self.speed
    def is_off_screen(self): return self.y > SCREEN_HEIGHT
    def get_rect(self): return pygame.Rect(self.x + 4, self.y + 4, self.width - 8, self.height - 8)

class Coin:
    def __init__(self):
        # TASK: Randomly generating weights (1, 3, or 5)
        self.weight = random.choice([1, 3, 5])
        # Visual size slightly depends on weight
        self.radius = 10 + self.weight 
        self.x = random.randint(ROAD_LEFT + 20, ROAD_RIGHT - 20)
        self.y = -self.radius
        self.speed = COIN_SPEED
        self.glow, self.glow_dir = 0, 1

    def draw(self, surface):
        # Change color based on weight for visibility
        color = YELLOW if self.weight == 1 else (255, 140, 0) if self.weight == 3 else (255, 69, 0)
        glow_color = (255, min(215 + self.glow, 255), 0)
        
        pygame.draw.circle(surface, glow_color, (int(self.x), int(self.y)), self.radius + 3)
        pygame.draw.circle(surface, color, (int(self.x), int(self.y)), self.radius)
        
        font = pygame.font.SysFont("Arial", 14, bold=True)
        label = font.render(str(self.weight), True, (255, 255, 255))
        surface.blit(label, (self.x - 5, self.y - 8))

    def update(self):
        self.y += self.speed
        self.glow += 5 * self.glow_dir
        if self.glow >= 40 or self.glow <= 0: self.glow_dir *= -1

    def is_off_screen(self): return self.y > SCREEN_HEIGHT
    def get_rect(self): return pygame.Rect(self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2)

class RoadMarkings:
    def __init__(self):
        self.line_positions = list(range(-40, SCREEN_HEIGHT + 40, 80))

    def update(self):
        for i in range(len(self.line_positions)):
            self.line_positions[i] += ROAD_SPEED
            if self.line_positions[i] > SCREEN_HEIGHT + 40: self.line_positions[i] = -40

    def draw(self, surface):
        for y in self.line_positions:
            pygame.draw.rect(surface, LINE_COLOR, (155, y, 6, 40))
            pygame.draw.rect(surface, LINE_COLOR, (235, y, 6, 40))