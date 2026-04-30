import pygame
import random

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
ROAD_LEFT = 60
ROAD_RIGHT = 340

BLUE = (50, 100, 220)
BLACK = (0, 0, 0)
YELLOW = (255, 215, 0)
WHITE = (255, 255, 255)

class PlayerCar:
    def __init__(self, color=BLUE):
        self.width, self.height = 40, 70
        self.x = SCREEN_WIDTH // 2 - self.width // 2
        self.y = SCREEN_HEIGHT - 120
        self.speed = 5
        self.color = color
        self.shield = False
        self.nitro_active = False

    def draw(self, surface):
        if self.shield:
            pygame.draw.rect(surface, (0, 255, 255), (self.x - 4, self.y - 4, self.width + 8, self.height + 8), 3, border_radius=10)
        
        # Твой оригинальный красивый дизайн!
        pygame.draw.rect(surface, self.color, (self.x, self.y, self.width, self.height), border_radius=6)
        pygame.draw.rect(surface, (150, 200, 255), (self.x + 6, self.y + 8, self.width - 12, 18), border_radius=3)
        pygame.draw.rect(surface, (150, 200, 255), (self.x + 6, self.y + 42, self.width - 12, 14), border_radius=3)
        for dx, dy in [(-6, 8), (self.width-4, 8), (-6, 44), (self.width-4, 44)]:
            pygame.draw.rect(surface, BLACK, (self.x + dx, self.y + dy, 10, 18), border_radius=3)

    def move(self, keys):
        s = self.speed * 1.5 if self.nitro_active else self.speed
        if keys[pygame.K_LEFT] and self.x > ROAD_LEFT + 5: self.x -= s
        if keys[pygame.K_RIGHT] and self.x + self.width < ROAD_RIGHT - 5: self.x += s
        if keys[pygame.K_UP] and self.y > 0: self.y -= s
        if keys[pygame.K_DOWN] and self.y + self.height < SCREEN_HEIGHT: self.y += s

    def get_rect(self):
        return pygame.Rect(self.x + 4, self.y + 4, self.width - 8, self.height - 8)

class EnemyCar:
    COLORS = [(220, 50, 50), (50, 180, 50), (200, 150, 0), (180, 50, 180)]
    def __init__(self, current_speed, player_x):
        self.width, self.height = 40, 70
        lanes = [80, 160, 240]
        player_lane = min(lanes, key=lambda l: abs(l - player_x))
        if player_lane in lanes: lanes.remove(player_lane)
        
        self.x = random.choice(lanes)
        self.y = -self.height
        self.speed = current_speed + random.uniform(-1, 2)
        self.color = random.choice(self.COLORS)

    def draw(self, surface):
        # Твой оригинальный красивый дизайн!
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
        self.weight = random.choice([1, 3, 5])
        self.radius = 12
        self.x = random.randint(ROAD_LEFT + 20, ROAD_RIGHT - 20)
        self.y = -self.radius
        self.speed = 5
        self.glow, self.glow_dir = 0, 1

    def draw(self, surface):
        # Вернули мерцание и оригинальную отрисовку!
        glow_color = (255, min(215 + self.glow, 255), 0)
        pygame.draw.circle(surface, glow_color, (int(self.x), int(self.y)), self.radius + 3)
        pygame.draw.circle(surface, YELLOW, (int(self.x), int(self.y)), self.radius)
        font = pygame.font.SysFont("Arial", 14, bold=True)
        label = font.render(str(self.weight), True, (180, 120, 0))
        surface.blit(label, (self.x - 5, self.y - 8))

    def update(self):
        self.y += self.speed
        self.glow += 5 * self.glow_dir
        if self.glow >= 40 or self.glow <= 0: self.glow_dir *= -1

    def is_off_screen(self): return self.y > SCREEN_HEIGHT
    def get_rect(self): return pygame.Rect(self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2)

class Obstacle:
    def __init__(self):
        self.type = random.choice(["oil", "barrier"])
        self.x = random.randint(ROAD_LEFT + 20, ROAD_RIGHT - 40)
        self.y = -50
        self.width, self.height = 40, 30

    def draw(self, surface):
        if self.type == "oil":
            pygame.draw.ellipse(surface, (40, 40, 40), (self.x, self.y, self.width, self.height))
        else:
            pygame.draw.rect(surface, (100, 100, 100), (self.x, self.y, self.width, self.height), border_radius=5)

    def update(self, speed): self.y += speed
    def get_rect(self): return pygame.Rect(self.x, self.y, self.width, self.height)

class PowerUp:
    TYPES = ["nitro", "shield", "repair"]
    def __init__(self):
        self.type = random.choice(self.TYPES)
        self.x = random.randint(ROAD_LEFT + 20, ROAD_RIGHT - 20)
        self.y = -30
        self.size = 25

    def draw(self, surface):
        color = (255, 50, 50) if self.type == "nitro" else (50, 200, 255) if self.type == "shield" else (50, 255, 50)
        pygame.draw.rect(surface, color, (self.x, self.y, self.size, self.size), border_radius=12) # Кругленькие бонусы
        f = pygame.font.SysFont("Arial", 15, bold=True)
        surface.blit(f.render(self.type[0].upper(), True, WHITE), (self.x + 7, self.y + 4))

    def update(self, speed): self.y += speed
    def get_rect(self): return pygame.Rect(self.x, self.y, self.size, self.size)

class RoadMarkings:
    def __init__(self):
        self.line_positions = list(range(-40, SCREEN_HEIGHT + 40, 80))
    def update(self):
        for i in range(len(self.line_positions)):
            self.line_positions[i] += 5
            if self.line_positions[i] > SCREEN_HEIGHT + 40: self.line_positions[i] = -40
    def draw(self, surface):
        for y in self.line_positions:
            pygame.draw.rect(surface, WHITE, (155, y, 6, 40))
            pygame.draw.rect(surface, WHITE, (235, y, 6, 40))