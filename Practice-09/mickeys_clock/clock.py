import pygame

class ClockHand:
    def __init__(self, image_path, center_pos, target_length):
        self.center_pos = center_pos
        
        # Загрузка оригинального изображения
        img = pygame.image.load(image_path).convert_alpha()
        original_w, original_h = img.get_size()
        
        # Автоматический расчет высоты для сохранения пропорций (никаких "шакалов")
        aspect_ratio = original_h / original_w
        target_height = int(target_length * aspect_ratio)
        
        self.original_image = pygame.transform.scale(img, (target_length, target_height))
        
        # Смещение для вращения за запястье (левый край картинки)
        self.offset = pygame.math.Vector2(target_length // 2, 0)

    def update(self, time_value, is_hours=False, extra_minutes=0):
        if is_hours:
            # 30 градусов на час + плавный сдвиг в зависимости от минут
            angle = (time_value % 12) * 30 + (extra_minutes / 60) * 30
        else:
            # 6 градусов на минуту
            angle = time_value * 6
        
        # Поворот (учитываем, что руки на картинках горизонтальные, поэтому +90)
        self.image = pygame.transform.rotate(self.original_image, -angle + 90)
        
        # Фиксация запястья в центре экрана
        rect_offset = self.offset.rotate(angle - 90)
        self.rect = self.image.get_rect(center=self.center_pos + rect_offset)

    def draw(self, screen):
        screen.blit(self.image, self.rect)