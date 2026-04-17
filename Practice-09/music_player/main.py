import pygame
import sys
import os
from player import MusicPlayer

def main():
    pygame.init()
    pygame.mixer.init()
    pygame.font.init()

    W, H = 800, 600
    screen = pygame.display.set_mode((W, H))
    pygame.display.set_caption("Compact Music Player")
    
    current_dir = os.path.dirname(__file__)
    
    # 1. Загрузка фона
    try:
        bg_img = pygame.image.load(os.path.join(current_dir, "background.jpg")).convert()
        bg_img = pygame.transform.scale(bg_img, (W, H))
    except:
        bg_img = None

    # 2. Стиль: Шрифты и Цвета
    # Выберем приятный цвет, например, Неоновый Голубой или Золотой
    ACCENT_COLOR = (255, 204, 0) # Золотистый/Оранжевый
    WHITE = (255, 255, 255)
    
    track_font = pygame.font.SysFont('Segoe UI', 30, bold=True)
    hint_font = pygame.font.SysFont('Segoe UI', 16)

    player = MusicPlayer(os.path.join(current_dir, "music"))

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if not pygame.mixer.music.get_busy() and not player.is_paused:
                        player.play()
                    else:
                        player.pause_unpause()
                elif event.key == pygame.K_s: player.stop()
                elif event.key == pygame.K_RIGHT: player.next_track()
                elif event.key == pygame.K_LEFT: player.prev_track()

        # --- ОТРИСОВКА ---
        if bg_img:
            screen.blit(bg_img, (0, 0))
            # Плашка внизу для читаемости текста
            panel = pygame.Surface((W, 120), pygame.SRCALPHA)
            panel.fill((0, 0, 0, 180)) # Полупрозрачный черный
            screen.blit(panel, (0, H - 120))
        else:
            screen.fill((20, 20, 20))

        # 3. Компактный текст СНИЗУ
        track_name = player.get_current_track_name()
        
        # Название трека
        name_surf = track_font.render(f"♪ {track_name}", True, ACCENT_COLOR)
        screen.blit(name_surf, (30, H - 90)) # Отступ слева 30, снизу 90

        # Подсказки (еще ниже и мельче)
        hints = "SPACE: Play/Pause  |  S: Stop  |  Arrows: Skip"
        hint_surf = hint_font.render(hints, True, (180, 180, 180))
        screen.blit(hint_surf, (30, H - 40))

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()