import pygame
import random

# ──────────────────────────────────────────
#  НАСТРОЙКИ И КОНСТАНТЫ
# ──────────────────────────────────────────
CELL_SIZE    = 20
COLS         = 25
ROWS         = 25
PANEL_HEIGHT = 60

SCREEN_WIDTH  = CELL_SIZE * COLS
SCREEN_HEIGHT = CELL_SIZE * ROWS + PANEL_HEIGHT

# ЦВЕТА
BLACK       = (0,   0,   0  )
WHITE       = (255, 255, 255)
GREEN       = (50,  200, 50 )
DARK_GREEN  = (30,  140, 30 )
HEAD_COLOR  = (20,  220, 20 )
RED         = (220, 50,  50 )
YELLOW      = (255, 215, 0  )
DARK_BG     = (15,  15,  25 )
GRID_COLOR  = (25,  25,  40 )
WALL_COLOR  = (80,  80,  100)
PANEL_COLOR = (10,  10,  20 )
PURPLE      = (160, 32,  240) # Новый цвет для тяжелой еды

# НАПРАВЛЕНИЯ
UP    = (0,  -1)
DOWN  = (0,   1)
LEFT  = (-1,  0)
RIGHT = (1,   0)

# НАСТРОЙКИ УРОВНЕЙ
BASE_SPEED       = 8
SPEED_INCREMENT  = 2
FOOD_PER_LEVEL   = 3
SCORE_PER_FOOD   = 10
FOOD_LIFETIME    = 5000 # Время жизни еды в миллисекундах (5 секунд)

# ──────────────────────────────────────────
#  КЛАСС: ЗМЕЙКА
# ──────────────────────────────────────────
class Snake:
    def __init__(self):
        start_x = COLS // 2
        start_y = ROWS // 2
        self.body      = [(start_x, start_y), (start_x - 1, start_y), (start_x - 2, start_y)]
        self.direction = RIGHT
        self.next_dir  = RIGHT
        self.grew      = False

    def set_direction(self, new_dir):
        opposite = (-self.direction[0], -self.direction[1])
        if new_dir != opposite:
            self.next_dir = new_dir

    def move(self):
        self.direction = self.next_dir
        head_x, head_y = self.body[0]
        dx, dy = self.direction
        new_head = (head_x + dx, head_y + dy)
        self.body.insert(0, new_head)
        if not self.grew:
            self.body.pop()
        else:
            self.grew = False

    def grow(self):
        self.grew = True

    def get_head(self):
        return self.body[0]

    def check_wall_collision(self):
        hx, hy = self.get_head()
        return hx < 0 or hx >= COLS or hy < 0 or hy >= ROWS

    def check_self_collision(self):
        return self.get_head() in self.body[1:]

    def draw(self, surface):
        for i, (cx, cy) in enumerate(self.body):
            px = cx * CELL_SIZE
            py = cy * CELL_SIZE + PANEL_HEIGHT
            if i == 0:
                pygame.draw.rect(surface, HEAD_COLOR, (px + 1, py + 1, CELL_SIZE - 2, CELL_SIZE - 2), border_radius=5)
                self._draw_eyes(surface, px, py)
            else:
                shade = max(50, 200 - i * 5)
                pygame.draw.rect(surface, (30, shade, 30), (px + 2, py + 2, CELL_SIZE - 4, CELL_SIZE - 4), border_radius=4)

    def _draw_eyes(self, surface, px, py):
        cx, cy = px + CELL_SIZE // 2, py + CELL_SIZE // 2
        if self.direction == RIGHT: eye1, eye2 = (cx + 4, cy - 4), (cx + 4, cy + 4)
        elif self.direction == LEFT: eye1, eye2 = (cx - 4, cy - 4), (cx - 4, cy + 4)
        elif self.direction == UP: eye1, eye2 = (cx - 4, cy - 4), (cx + 4, cy - 4)
        else: eye1, eye2 = (cx - 4, cy + 4), (cx + 4, cy + 4)
        for e in [eye1, eye2]:
            pygame.draw.circle(surface, WHITE, e, 3)
            pygame.draw.circle(surface, BLACK, e, 1)

# ──────────────────────────────────────────
#  КЛАСС: ЕДА
# ──────────────────────────────────────────
class Food:
    def __init__(self):
        self.pos        = (0, 0)
        self.pulse      = 0
        self.pulse_dir  = 1
        self.weight     = 1          # Вес еды (множитель очков)
        self.spawn_time = 0          # Время появления для таймера
        self.color      = RED        # Цвет зависит от веса

    def respawn(self, snake_body):
        while True:
            x, y = random.randint(0, COLS - 1), random.randint(0, ROWS - 1)
            if (x, y) not in snake_body:
                self.pos = (x, y)
                break
        
        # Генерация случайного веса (1, 2 или 3)
        # 70% шанс - веса 1, 20% - веса 2, 10% - веса 3
        chance = random.random()
        if chance < 0.7:
            self.weight = 1
            self.color = RED
        elif chance < 0.9:
            self.weight = 2
            self.color = YELLOW
        else:
            self.weight = 3
            self.color = PURPLE
            
        # Фиксируем время появления еды
        self.spawn_time = pygame.time.get_ticks()

    def update(self, snake_body):
        # Анимация пульсации
        self.pulse += 3 * self.pulse_dir
        if self.pulse >= 30 or self.pulse <= 0: self.pulse_dir *= -1
        
        # Проверка таймера: если прошло больше FOOD_LIFETIME, еда переспавнится
        current_time = pygame.time.get_ticks()
        if current_time - self.spawn_time > FOOD_LIFETIME:
            self.respawn(snake_body)

    def draw(self, surface):
        cx = self.pos[0] * CELL_SIZE + CELL_SIZE // 2
        cy = self.pos[1] * CELL_SIZE + CELL_SIZE // 2 + PANEL_HEIGHT
        
        # Размер визуально увеличивается в зависимости от веса
        r = (7 + self.pulse // 15) + (self.weight * 2) 
        
        pygame.draw.circle(surface, self.color, (cx, cy), r)
        pygame.draw.circle(surface, (255, 255, 255), (cx - 2, cy - 2), r // 3, 1) # Блик
        
        # Рисуем хвостик (листок)
        pygame.draw.line(surface, DARK_GREEN, (cx, cy - r), (cx + 3, cy - r - 5), 2)
        
        # Визуальный таймер (тонкая полоска под едой)
        time_left = max(0, FOOD_LIFETIME - (pygame.time.get_ticks() - self.spawn_time))
        bar_width = int((CELL_SIZE - 4) * (time_left / FOOD_LIFETIME))
        if bar_width > 0:
            pygame.draw.rect(surface, WHITE, (cx - (CELL_SIZE//2) + 2, cy + r + 2, bar_width, 2))