import pygame
import sys
from snake_objects import *

# Инициализация
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snake 🐍")
clock = pygame.time.Clock()

def draw_grid(surface):
    for x in range(COLS):
        for y in range(ROWS):
            rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE + PANEL_HEIGHT, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(surface, GRID_COLOR, rect, 1)

def draw_panel(surface, score, level, food_count):
    pygame.draw.rect(surface, PANEL_COLOR, (0, 0, SCREEN_WIDTH, PANEL_HEIGHT))
    pygame.draw.line(surface, WALL_COLOR, (0, PANEL_HEIGHT), (SCREEN_WIDTH, PANEL_HEIGHT), 2)
    font = pygame.font.SysFont("Arial", 20, bold=True)
    
    surface.blit(font.render(f"Уровень: {level}", True, YELLOW), (10, 8))
    surface.blit(font.render(f"Очки: {score}", True, WHITE), (SCREEN_WIDTH // 2 - 40, 8))
    
    food_in_level = food_count % FOOD_PER_LEVEL
    prog_text = font.render(f"До ур.: {food_in_level}/{FOOD_PER_LEVEL}", True, GREEN)
    surface.blit(prog_text, (SCREEN_WIDTH - prog_text.get_width() - 10, 8))

    bar_w, bar_x, bar_y = 120, SCREEN_WIDTH // 2 - 60, 36
    pygame.draw.rect(surface, (50, 50, 50), (bar_x, bar_y, bar_w, 10), border_radius=5)
    fill = int(bar_w * food_in_level / FOOD_PER_LEVEL)
    if fill > 0: pygame.draw.rect(surface, GREEN, (bar_x, bar_y, fill, 10), border_radius=5)
    pygame.draw.rect(surface, WHITE, (bar_x, bar_y, bar_w, 10), 1, border_radius=5)

def show_message(surface, title, color, score, level, hint):
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    surface.blit(overlay, (0, 0))
    f_big, f_med, f_small = pygame.font.SysFont("Arial", 48, bold=True), pygame.font.SysFont("Arial", 26), pygame.font.SysFont("Arial", 18)
    
    t1 = f_big.render(title, True, color)
    surface.blit(t1, (SCREEN_WIDTH // 2 - t1.get_width() // 2, 180))
    t2 = f_med.render(f"Очки: {score}  |  Уровень: {level}", True, YELLOW)
    surface.blit(t2, (SCREEN_WIDTH // 2 - t2.get_width() // 2, 260))
    t3 = f_small.render(hint, True, (200, 200, 200))
    surface.blit(t3, (SCREEN_WIDTH // 2 - t3.get_width() // 2, 320))
    pygame.display.flip()

def game_loop():
    snake, food = Snake(), Food()
    food.respawn(snake.body)
    score, level, food_count, speed = 0, 1, 0, BASE_SPEED
    game_over = False

    while True:
        clock.tick(speed)
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: pygame.quit(); sys.exit()
                if not game_over:
                    if event.key in [pygame.K_UP, pygame.K_w]: snake.set_direction(UP)
                    if event.key in [pygame.K_DOWN, pygame.K_s]: snake.set_direction(DOWN)
                    if event.key in [pygame.K_LEFT, pygame.K_a]: snake.set_direction(LEFT)
                    if event.key in [pygame.K_RIGHT, pygame.K_d]: snake.set_direction(RIGHT)
                if game_over and event.key == pygame.K_r: return game_loop()

        if game_over:
            show_message(screen, "GAME OVER", RED, score, level, "R — снова  |  ESC — выход")
            continue

        snake.move()
        if snake.check_wall_collision() or snake.check_self_collision():
            game_over = True
            continue

        # Проверка поедания еды
        if snake.get_head() == food.pos:
            snake.grow()
            # Очки теперь зависят от веса съеденной еды
            score += (SCORE_PER_FOOD * level) * food.weight
            food_count += 1
            food.respawn(snake.body)
            
            if food_count % FOOD_PER_LEVEL == 0:
                level += 1
                speed = BASE_SPEED + (level - 1) * SPEED_INCREMENT
                draw_panel(screen, score, level, food_count)
                show_message(screen, f"УРОВЕНЬ {level}!", YELLOW, score, level, "Продолжай!")
                pygame.time.delay(1200)

        # Передаем тело змейки в update, чтобы еда не спавнилась внутри неё при исчезновении по таймеру
        food.update(snake.body)
        
        screen.fill(DARK_BG)
        draw_grid(screen)
        pygame.draw.rect(screen, WALL_COLOR, (0, PANEL_HEIGHT, SCREEN_WIDTH, SCREEN_HEIGHT - PANEL_HEIGHT), 3)
        food.draw(screen)
        snake.draw(screen)
        draw_panel(screen, score, level, food_count)
        pygame.display.flip()

def start_screen():
    f_title, f_sub, f_hint = pygame.font.SysFont("Arial", 52, bold=True), pygame.font.SysFont("Arial", 20), pygame.font.SysFont("Arial", 17)
    while True:
        screen.fill(DARK_BG)
        t = f_title.render("SNAKE 🐍", True, GREEN)
        screen.blit(t, (SCREEN_WIDTH // 2 - t.get_width() // 2, 140))
        lines = ["Ешь еду, расти, не врезайся!", "Каждые 3 еды — новый уровень", "Очки × уровень", "", "Управление: стрелки или WASD", "ESC — выход"]
        for i, line in enumerate(lines):
            color = YELLOW if i == 1 else (180, 180, 180)
            screen.blit(f_sub.render(line, True, color), (SCREEN_WIDTH // 2 - 120, 230 + i * 28))
        screen.blit(f_hint.render("Нажми ENTER чтобы начать", True, WHITE), (SCREEN_WIDTH // 2 - 100, 420))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN: return
                if event.key == pygame.K_ESCAPE: pygame.quit(); sys.exit()

if __name__ == "__main__":
    start_screen()
    game_loop()