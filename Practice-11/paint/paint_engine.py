import pygame

# Константы
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 950 # Увеличили высоту, чтобы палитра не накладывалась
TOOLBAR_W = 220
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PANEL_BG = (55, 55, 60)
DARK_GRAY = (40, 40, 45)
HIGHLIGHT = (0, 120, 215)

# Инструменты
TOOL_BRUSH = "brush"
TOOL_RECT = "rect"
TOOL_CIRCLE = "circle"
TOOL_ERASER = "eraser"
TOOL_SQUARE = "square"
TOOL_R_TRIANGLE = "r_triangle"
TOOL_E_TRIANGLE = "e_triangle"
TOOL_RHOMBUS = "rhombus"

PALETTE = [
    (0, 0, 0), (128, 128, 128), (255, 255, 255),
    (255, 0, 0), (0, 255, 0), (0, 0, 255),
    (255, 255, 0), (255, 165, 0), (128, 0, 128)
]

class Button:
    def __init__(self, x, y, w, h, text, tool_id):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.tool_id = tool_id

    def draw(self, surface, font, is_active):
        bg = HIGHLIGHT if is_active else DARK_GRAY
        pygame.draw.rect(surface, bg, self.rect, border_radius=8)
        txt = font.render(self.text, True, WHITE)
        surface.blit(txt, (self.rect.centerx - txt.get_width()//2, self.rect.centery - txt.get_height()//2))

class PaintApp:
    def __init__(self):
        self.canvas = pygame.Surface((SCREEN_WIDTH - TOOLBAR_W, SCREEN_HEIGHT))
        self.canvas.fill(WHITE)
        self.tool = TOOL_BRUSH
        self.color = BLACK
        self.brush_size = 5
        self.drawing = False
        self.start_pos = None
        self.last_pos = None

        # Создаем кнопки
        tools = [("Кисть", TOOL_BRUSH), ("Ластик", TOOL_ERASER), ("Прямоуг.", TOOL_RECT), 
                 ("Круг", TOOL_CIRCLE), ("Квадрат", TOOL_SQUARE), ("Пр. Треуг.", TOOL_R_TRIANGLE),
                 ("Равн. Треуг.", TOOL_E_TRIANGLE), ("Ромб", TOOL_RHOMBUS)]
        self.tool_buttons = [Button(20, 70 + i*45, 180, 40, t[0], t[1]) for i, t in enumerate(tools)]
        self.clear_btn = Button(20, SCREEN_HEIGHT - 60, 180, 40, "ОЧИСТИТЬ", "clear")
        self.size_buttons = [(pygame.Rect(25 + i*45, SCREEN_HEIGHT - 130, 35, 35), s) for i, s in enumerate([4, 8, 16, 32])]

    def handle_panel_click(self, pos):
        for btn in self.tool_buttons:
            if btn.rect.collidepoint(pos): self.tool = btn.tool_id
        if self.clear_btn.rect.collidepoint(pos): self.canvas.fill(WHITE)
        
        # Клик по палитре (координаты должны совпадать с отрисовкой в main)
        palette_y = 460
        for i, color in enumerate(PALETTE):
            r, c = i // 3, i % 3
            if pygame.Rect(25 + c * 55, palette_y + r * 55, 45, 45).collidepoint(pos):
                self.color = color
        for rect, s in self.size_buttons:
            if rect.collidepoint(pos): self.brush_size = s

    def mouse_down(self, pos):
        self.drawing = True
        self.start_pos = (pos[0] - TOOLBAR_W, pos[1])
        self.last_pos = self.start_pos

    def mouse_up(self, pos):
        if self.drawing and self.tool not in [TOOL_BRUSH, TOOL_ERASER]:
            end = (pos[0] - TOOLBAR_W, pos[1])
            self.draw_shape(end)
        self.drawing = False

    def mouse_move(self, pos):
        if self.drawing and self.tool in [TOOL_BRUSH, TOOL_ERASER]:
            curr = (pos[0] - TOOLBAR_W, pos[1])
            col = WHITE if self.tool == TOOL_ERASER else self.color
            sz = self.brush_size * 3 if self.tool == TOOL_ERASER else self.brush_size
            pygame.draw.line(self.canvas, col, self.last_pos, curr, sz * 2)
            pygame.draw.circle(self.canvas, col, curr, sz)
            self.last_pos = curr

    def draw_shape(self, end):
        x1, y1 = self.start_pos
        x2, y2 = end
        dx, dy = x2 - x1, y2 - y1
        
        # Общие параметры для всех фигур
        rect_x = min(x1, x2)
        rect_y = min(y1, y2)
        rect_w = abs(dx)
        rect_h = abs(dy)

        if self.tool == TOOL_RECT:
            # Рисуем прямоугольник
            pygame.draw.rect(self.canvas, self.color, (rect_x, rect_y, rect_w, rect_h), self.brush_size)
            
        elif self.tool == TOOL_SQUARE:
            # Рисуем квадрат
            side = max(rect_w, rect_h)
            # Определяем координаты так, чтобы квадрат рос от точки нажатия
            sq_x = x1 if dx > 0 else x1 - side
            sq_y = y1 if dy > 0 else y1 - side
            pygame.draw.rect(self.canvas, self.color, (sq_x, sq_y, side, side), self.brush_size)
            
        elif self.tool == TOOL_CIRCLE:
            # Рисуем эллипс
            if rect_w > 0 and rect_h > 0: # Проверка, чтобы не упало при нулевом размере
                pygame.draw.ellipse(self.canvas, self.color, (rect_x, rect_y, rect_w, rect_h), self.brush_size)
                
        elif self.tool == TOOL_R_TRIANGLE:
            # Прямоугольный треугольник
            pygame.draw.polygon(self.canvas, self.color, [(x1, y1), (x1, y2), (x2, y2)], self.brush_size)
            
        elif self.tool == TOOL_E_TRIANGLE:
            # Равнобедренный треугольник (вписанный в прямоугольник)
            pygame.draw.polygon(self.canvas, self.color, [(x1 + dx//2, y1), (x1, y2), (x2, y2)], self.brush_size)
            
        elif self.tool == TOOL_RHOMBUS:
            # Ромб
            pts = [
                (x1 + dx//2, y1), # верх
                (x2, y1 + dy//2), # право
                (x1 + dx//2, y2), # низ
                (x1, y1 + dy//2)  # лево
            ]
            pygame.draw.polygon(self.canvas, self.color, pts, self.brush_size)