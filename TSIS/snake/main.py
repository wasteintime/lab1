import pygame
import sys
import os
import json
import random
from snake_objects import *
from db import *

# ──────────────────────────────────────────
#  ИНИЦИАЛИЗАЦИЯ И НАСТРОЙКИ
# ──────────────────────────────────────────
BASE_DIR = os.path.join("tsis", "snake")
if not os.path.exists(BASE_DIR):
    os.makedirs(BASE_DIR)

SETTINGS_PATH = os.path.join(BASE_DIR, "settings.json")

def load_settings():
    if os.path.exists(SETTINGS_PATH):
        with open(SETTINGS_PATH, "r") as f:
            return json.load(f)
    return {"snake_color": [50, 200, 50], "grid_on": True, "sound_on": True}

def save_settings(new_settings):
    with open(SETTINGS_PATH, "w") as f:
        json.dump(new_settings, f)

pygame.init()
current_settings = load_settings()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snake Pro: Narxoz Edition")
clock = pygame.time.Clock()

# Шрифты
FONT_BIG = pygame.font.SysFont("Arial", 48, bold=True)
FONT_MED = pygame.font.SysFont("Arial", 28, bold=True)
FONT_SMALL = pygame.font.SysFont("Arial", 20)

# ──────────────────────────────────────────
#  UI КОМПОНЕНТЫ (КНОПКИ)
# ──────────────────────────────────────────
def draw_button(text, x, y, w, h, inactive_color, active_color):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    
    rect = pygame.Rect(x, y, w, h)
    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(screen, active_color, rect, border_radius=10)
        if click[0] == 1:
            return True
    else:
        pygame.draw.rect(screen, inactive_color, rect, border_radius=10)
    
    txt_surf = FONT_SMALL.render(text, True, WHITE)
    screen.blit(txt_surf, (x + (w // 2 - txt_surf.get_width() // 2), y + (h // 2 - txt_surf.get_height() // 2)))
    return False
def draw_panel(surface, score, level, food_count, username, best):
    # Фон верхней панели
    pygame.draw.rect(surface, PANEL_COLOR, (0, 0, SCREEN_WIDTH, PANEL_HEIGHT))
    pygame.draw.line(surface, WALL_COLOR, (0, PANEL_HEIGHT), (SCREEN_WIDTH, PANEL_HEIGHT), 2)
    
    # Тексты (используем те же шрифты, что инициализировали ранее)
    u_txt = FONT_SMALL.render(f"Игрок: {username}", True, WHITE)
    b_txt = FONT_SMALL.render(f"Рекорд: {best}", True, YELLOW)
    l_txt = FONT_SMALL.render(f"Уровень: {level}", True, WHITE)
    s_txt = FONT_SMALL.render(f"Очки: {score}", True, GREEN)
    
    surface.blit(u_txt, (10, 5))
    surface.blit(b_txt, (10, 30))
    surface.blit(l_txt, (SCREEN_WIDTH // 2 - 40, 5))
    surface.blit(s_txt, (SCREEN_WIDTH - s_txt.get_width() - 10, 5))

    # Твой фирменный прогресс-бар до следующего уровня
    food_in_level = food_count % FOOD_PER_LEVEL
    bar_w, bar_x, bar_y = 120, SCREEN_WIDTH // 2 - 60, 36
    pygame.draw.rect(surface, (50, 50, 50), (bar_x, bar_y, bar_w, 10), border_radius=5)
    fill = int(bar_w * food_in_level / FOOD_PER_LEVEL)
    if fill > 0: 
        pygame.draw.rect(surface, GREEN, (bar_x, bar_y, fill, 10), border_radius=5)
    pygame.draw.rect(surface, WHITE, (bar_x, bar_y, bar_w, 10), 1, border_radius=5)

def draw_grid(surface):
    # Проверяем настройку из JSON
    if not current_settings.get("grid_on", True): 
        return
    
    for x in range(COLS):
        for y in range(ROWS):
            # Смещение на PANEL_HEIGHT, чтобы сетка была под игровой панелью
            rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE + PANEL_HEIGHT, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(surface, GRID_COLOR, rect, 1)
# ──────────────────────────────────────────
#  ЭКРАНЫ
# ──────────────────────────────────────────

def main_menu():
    username = ""
    # Сначала ввод имени, если его нет
    while not username:
        username = input_username_screen()

    while True:
        screen.fill(DARK_BG)
        title = FONT_BIG.render("SNAKE TSIS 4", True, GREEN)
        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 80))

        if draw_button("ИГРАТЬ", SCREEN_WIDTH // 2 - 100, 200, 200, 50, (40, 40, 60), (60, 60, 100)):
            game_loop(username)
        
        if draw_button("РЕКОРДЫ", SCREEN_WIDTH // 2 - 100, 270, 200, 50, (40, 40, 60), (60, 60, 100)):
            leaderboard_screen()

        if draw_button("НАСТРОЙКИ", SCREEN_WIDTH // 2 - 100, 340, 200, 50, (40, 40, 60), (60, 60, 100)):
            settings_screen()

        if draw_button("ВЫХОД", SCREEN_WIDTH // 2 - 100, 410, 200, 50, (100, 40, 40), (150, 50, 50)):
            pygame.quit(); sys.exit()

        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()

def settings_screen():
    global current_settings
    while True:
        screen.fill(DARK_BG)
        title = FONT_MED.render("НАСТРОЙКИ", True, YELLOW)
        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 50))

        # Переключатель сетки
        grid_status = "ВКЛ" if current_settings["grid_on"] else "ВЫКЛ"
        if draw_button(f"Сетка: {grid_status}", 100, 150, 300, 50, (50, 50, 70), (80, 80, 120)):
            current_settings["grid_on"] = not current_settings["grid_on"]
            pygame.time.delay(150)

        # Выбор цвета (упрощенно)
        if draw_button("Цвет змейки: GREEN", 100, 220, 300, 50, GREEN, DARK_GREEN):
            current_settings["snake_color"] = [50, 200, 50]
        if draw_button("Цвет змейки: BLUE", 100, 290, 300, 50, (50, 50, 200), (30, 30, 150)):
            current_settings["snake_color"] = [50, 50, 200]

        if draw_button("СОХРАНИТЬ И НАЗАД", SCREEN_WIDTH // 2 - 120, 450, 240, 50, (40, 100, 40), (50, 150, 50)):
            save_settings(current_settings)
            return

        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()

def input_username_screen():
    uname = ""
    while True:
        screen.fill(DARK_BG)
        txt = FONT_MED.render("Введите ваш ник:", True, WHITE)
        screen.blit(txt, (SCREEN_WIDTH // 2 - txt.get_width() // 2, 200))
        
        val_surf = FONT_BIG.render(uname + "_", True, GREEN)
        screen.blit(val_surf, (SCREEN_WIDTH // 2 - val_surf.get_width() // 2, 260))
        
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and uname: return uname
                elif event.key == pygame.K_BACKSPACE: uname = uname[:-1]
                else:
                    if len(uname) < 10 and event.unicode.isalnum(): uname += event.unicode
def leaderboard_screen():
    while True:
        screen.fill(DARK_BG)
        title = FONT_MED.render("ТАБЛИЦА РЕКОРДОВ", True, YELLOW)
        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 50))
        
        try:
            # Пытаемся достать данные из PostgreSQL (из твоего db.py)
            scores = get_top_scores() 
            if not scores:
                empty_txt = FONT_SMALL.render("Пока тут пусто...", True, WHITE)
                screen.blit(empty_txt, (SCREEN_WIDTH // 2 - empty_txt.get_width() // 2, 200))
            else:
                for i, (name, sc, lvl, date) in enumerate(scores):
                    txt = f"{i+1}. {name} — {sc} очков (Ур. {lvl})"
                    row = FONT_SMALL.render(txt, True, WHITE)
                    screen.blit(row, (100, 120 + i * 30))
        except Exception as e:
            error_txt = FONT_SMALL.render("Ошибка подключения к БД", True, RED)
            screen.blit(error_txt, (SCREEN_WIDTH // 2 - error_txt.get_width() // 2, 200))

        # Кнопка назад
        if draw_button("НАЗАД", SCREEN_WIDTH // 2 - 100, 500, 200, 50, (40, 40, 60), (60, 60, 100)):
            return # Возвращаемся в главное меню

        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
def game_over_screen(username, score, level):
    # Пытаемся получить рекорд из базы данных
    best = get_personal_best(username)
    
    while True:
        screen.fill((40, 10, 10))  # Темно-красный фон для Game Over
        
        msg = FONT_BIG.render("GAME OVER", True, RED)
        screen.blit(msg, (SCREEN_WIDTH // 2 - msg.get_width() // 2, 100))
        
        info = FONT_SMALL.render(f"Игрок: {username}  |  Счет: {score}  |  Уровень: {level}", True, WHITE)
        screen.blit(info, (SCREEN_WIDTH // 2 - info.get_width() // 2, 200))
        
        best_txt = FONT_MED.render(f"Ваш рекорд: {best}", True, YELLOW)
        screen.blit(best_txt, (SCREEN_WIDTH // 2 - best_txt.get_width() // 2, 250))

        # Кнопка возврата в меню
        if draw_button("В МЕНЮ", SCREEN_WIDTH // 2 - 100, 350, 200, 50, (60, 40, 40), (100, 50, 50)):
            return  # Выход из функции вернет нас в main_menu

        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

# ──────────────────────────────────────────
#  ГЕЙМПЛЕЙ (Логика из прошлого шага)
# ──────────────────────────────────────────
def game_loop(username):
    # Инициализация объектов
    snake = Snake()
    snake.body_color = current_settings["snake_color"]
    food = Food()
    poison = Poison()
    powerup = PowerUp()
    obstacles = Obstacles()
    
    score, level, food_count = 0, 1, 0
    speed = BASE_SPEED
    personal_best = get_personal_best(username) # Из db.py
    shield_active = False
    
    def get_forbidden():
        return set(snake.body) | set(obstacles.blocks) | {food.pos} | {poison.pos}

    food.respawn(get_forbidden())
    poison.respawn(get_forbidden())

    running = True
    while running:
        # 1. События
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_UP, pygame.K_w]: snake.set_direction(UP)
                if event.key in [pygame.K_DOWN, pygame.K_s]: snake.set_direction(DOWN)
                if event.key in [pygame.K_LEFT, pygame.K_a]: snake.set_direction(LEFT)
                if event.key in [pygame.K_RIGHT, pygame.K_d]: snake.set_direction(RIGHT)
                if event.key == pygame.K_ESCAPE: return # Возврат в меню

        # 2. Логика бонусов (Power-ups)
        if not powerup.active and random.random() < 0.01:
            powerup.spawn(get_forbidden())
        if powerup.active and pygame.time.get_ticks() - powerup.spawn_time > 8000:
            powerup.active = False

        # 3. Движение
        snake.move()
        head = snake.get_head()

        # 4. Проверка столкновений (Стены, Препятствия, Хвост)
        if snake.check_wall_collision() or head in obstacles.blocks or snake.check_self_collision():
            if shield_active:
                shield_active = False # Щит спасает один раз
            else:
                save_score(username, score, level) # Сохраняем в БД
                game_over_screen(username, score, level)
                return

        # 5. Поедание еды
        if head == food.pos:
            snake.grow()
            score += (SCORE_PER_FOOD * level) * food.weight
            food_count += 1
            food.respawn(get_forbidden())
            
            # Повышение уровня
            if food_count % FOOD_PER_LEVEL == 0:
                level += 1
                speed += SPEED_INCREMENT
                obstacles.generate(level, snake.body) # Новые блоки с 3-го уровня

        # 6. Ядовитая еда
        if head == poison.pos:
            if len(snake.body) > 2:
                snake.body.pop()
                snake.body.pop()
                poison.respawn(get_forbidden())
            else:
                save_score(username, score, level)
                game_over_screen(username, score, level)
                return

        # 7. Подбор бонуса
        if powerup.active and head == powerup.pos:
            if powerup.type == 'speed': speed += 4
            elif powerup.type == 'slow': speed = max(5, speed - 3)
            elif powerup.type == 'shield': shield_active = True
            powerup.active = False

        # 8. Отрисовка (Твой стиль)
        screen.fill(DARK_BG)
        draw_grid(screen)
        obstacles.draw(screen)
        food.update(snake.body) # Обновление таймера и анимации еды
        food.draw(screen)
        poison.draw(screen)
        powerup.draw(screen)
        snake.draw(screen)
        
        if shield_active: # Визуальный эффект щита
            px = head[0] * CELL_SIZE
            py = head[1] * CELL_SIZE + PANEL_HEIGHT
            pygame.draw.rect(screen, WHITE, (px, py, CELL_SIZE, CELL_SIZE), 2)

        draw_panel(screen, score, level, food_count, username, personal_best)
        pygame.display.flip()
        clock.tick(speed)

# Запуск
if __name__ == "__main__":
    main_menu()