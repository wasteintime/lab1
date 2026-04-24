import pygame
import sys
from racer_entities import *

# Цвета для UI
WHITE = (255, 255, 255)
DARK_GRAY = (30, 30, 30)
RED = (220, 50, 50)
ROAD_COLOR = (60, 60, 60)
YELLOW = (255, 215, 0)

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Racer Game 🚗")
clock = pygame.time.Clock()

def show_game_over(surface, coins):
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 170))
    surface.blit(overlay, (0, 0))
    
    f_big = pygame.font.SysFont("Arial", 52, bold=True)
    f_med = pygame.font.SysFont("Arial", 28)
    
    surface.blit(f_big.render("GAME OVER", True, RED), (SCREEN_WIDTH//2 - 140, 180))
    surface.blit(f_med.render(f"Монет собрано: {coins}", True, YELLOW), (SCREEN_WIDTH//2 - 110, 270))
    pygame.display.flip()
    
    # Цикл ожидания после смерти
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r: return True # Флаг на рестарт
                if event.key == pygame.K_ESCAPE: pygame.quit(); sys.exit()
    return False

def game_loop():
    player, road = PlayerCar(), RoadMarkings()
    enemies, coins, coin_count, frame_count = [], [], 0, 0
    font_ui = pygame.font.SysFont("Arial", 22, bold=True)
    
    while True:
        clock.tick(60)
        frame_count += 1
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()

        # Спавн объектов
        if frame_count % 60 == 0: enemies.append(EnemyCar())
        if frame_count % 90 == 0: coins.append(Coin())

        # Логика движения
        player.move(pygame.key.get_pressed())
        road.update()
        for e in enemies: e.update()
        for c in coins: c.update()

        # Удаление лишнего
        enemies = [e for e in enemies if not e.is_off_screen()]
        coins = [c for c in coins if not c.is_off_screen()]

        # Проверка коллизий
        p_rect = player.get_rect()
        
        # Столкновение с врагом
        for e in enemies:
            if p_rect.colliderect(e.get_rect()):
                if show_game_over(screen, coin_count): 
                    return game_loop() # Рестарт
                else: 
                    return

        # Сбор монет
        for c in coins[:]:
            if p_rect.colliderect(c.get_rect()):
                coins.remove(c)
                coin_count += 1

        # Отрисовка
        screen.fill((34, 120, 34)) # Трава
        pygame.draw.rect(screen, ROAD_COLOR, (ROAD_LEFT, 0, ROAD_RIGHT - ROAD_LEFT, SCREEN_HEIGHT))
        
        road.draw(screen)
        for e in enemies: e.draw(screen)
        for c in coins: c.draw(screen)
        player.draw(screen)
        
        # Счётчик монет
        label = font_ui.render(f"🪙 Монеты: {coin_count}", True, YELLOW)
        screen.blit(label, (SCREEN_WIDTH - 150, 12))
        
        pygame.display.flip()

def start_screen():
    while True:
        screen.fill(DARK_GRAY)
        f_title = pygame.font.SysFont("Arial", 48, bold=True)
        title = f_title.render("RACER 🚗", True, WHITE)
        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 200))
        
        f_hint = pygame.font.SysFont("Arial", 18)
        hint = f_hint.render("Нажми ENTER для старта", True, WHITE)
        screen.blit(hint, (SCREEN_WIDTH // 2 - hint.get_width() // 2, 300))
        
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN: return
                if event.key == pygame.K_ESCAPE: pygame.quit(); sys.exit()

if __name__ == "__main__":
    start_screen()
    game_loop()