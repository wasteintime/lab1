import pygame
import datetime
import os
import sys
from clock import ClockHand

def main():
    pygame.init()
    
    # Размер окна 800x800
    SIZE = 800
    screen = pygame.display.set_mode((SIZE, SIZE))
    pygame.display.set_caption("Mickey's Classic Clock")
    center = (SIZE // 2, SIZE // 2)
    clock = pygame.time.Clock()

    # Пути
    current_dir = os.path.dirname(__file__)
    img_dir = os.path.join(current_dir, "images")

    try:
        # Фон
        bg = pygame.image.load(os.path.join(img_dir, "main-clock.png")).convert_alpha()
        bg = pygame.transform.scale(bg, (SIZE, SIZE))

        # Создаем только две классические руки (без цвета)
        # Часовая стрелка (левая рука) — короче
        hour_hand = ClockHand(os.path.join(img_dir, "left-hand.png"), center, 260)
        # Минутная стрелка (правая рука) — длиннее
        minute_hand = ClockHand(os.path.join(img_dir, "right-hand.png"), center, 370)
        
    except Exception as e:
        print(f"Ошибка загрузки изображений: {e}")
        return

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Работаем со временем
        t = datetime.datetime.now()

        # Обновляем логику стрелок
        hour_hand.update(t.hour, is_hours=True, extra_minutes=t.minute)
        minute_hand.update(t.minute)

        # Отрисовка
        screen.fill((255, 255, 255))
        screen.blit(bg, (0, 0))
        
        hour_hand.draw(screen)
        minute_hand.draw(screen)

        # Декоративная точка в центре
        pygame.draw.circle(screen, (0, 0, 0), center, 12)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()