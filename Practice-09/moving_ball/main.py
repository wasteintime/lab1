import pygame
import sys
from ball import Ball

def main():
    pygame.init()
    
    # Настройки экрана
    W, H = 800, 600
    screen = pygame.display.set_mode((W, H))
    pygame.display.set_caption("Moving Ball Task")
    
    # Цвета
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    
    # Создаем объект мяча в центре экрана
    my_ball = Ball(W // 2, H // 2, 25, RED, W, H)
    
    clock = pygame.time.Clock()

    running = True
    while running:
        screen.fill(WHITE)  # Очистка экрана
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            # Обработка ОДИНОЧНЫХ нажатий
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    my_ball.move(0, -1)
                elif event.key == pygame.K_DOWN:
                    my_ball.move(0, 1)
                elif event.key == pygame.K_LEFT:
                    my_ball.move(-1, 0)
                elif event.key == pygame.K_RIGHT:
                    my_ball.move(1, 0)

        # Рисуем мяч
        my_ball.draw(screen)
        
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()