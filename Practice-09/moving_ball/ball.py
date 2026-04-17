import pygame

class Ball:
    def __init__(self, x, y, radius, color, screen_width, screen_height):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.sw = screen_width
        self.sh = screen_height
        self.step = 20  # Скорость прыжка мяча

    def move(self, dx, dy):
        """
        Метод для перемещения мяча с проверкой границ.
        dx, dy — это направление (-1, 0, 1)
        """
        new_x = self.x + dx * self.step
        new_y = self.y + dy * self.step

        # Проверка границ: центр мяча должен быть не ближе радиуса к краю
        if self.radius <= new_x <= self.sw - self.radius:
            self.x = new_x
        if self.radius <= new_y <= self.sh - self.radius:
            self.y = new_y

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)