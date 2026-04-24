import pygame

# --- КОНСТАНТЫ РАЗМЕРОВ ---
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
TOOLBAR_W = 220  # Немного расширил для удобства
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PANEL_BG = (60, 60, 70)
DARK_GRAY = (40, 40, 45)
HIGHLIGHT = (0, 120, 215)

# Инструменты
TOOL_BRUSH = "brush"
TOOL_RECT = "rect"
TOOL_CIRCLE = "circle"
TOOL_ERASER = "eraser"

# Палитра
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
        txt_surf = font.render(self.text, True, WHITE)
        surface.blit(txt_surf, (self.rect.centerx - txt_surf.get_width()//2, 
                                self.rect.centery - txt_surf.get_height()//2))

class PaintApp:
    def __init__(self):
        self.canvas = pygame.Surface((SCREEN_WIDTH - TOOLBAR_W, SCREEN_HEIGHT))
        self.canvas.fill(WHITE)
        self.tool = TOOL_BRUSH
        self.color = BLACK
        self.brush_size = 5
        self.drawing = False
        self.start_pos = None
        
        # Кнопки инструментов
        self.tool_buttons = [
            Button(20, 80, 180, 40, "Кисть (B)", TOOL_BRUSH),
            Button(20, 130, 180, 40, "Прямоугольник (R)", TOOL_RECT),
            Button(20, 180, 180, 40, "Круг (C)", TOOL_CIRCLE),
            Button(20, 230, 180, 40, "Ластик (E)", TOOL_ERASER),
        ]
        
        # Кнопка очистки
        self.clear_btn = Button(20, SCREEN_HEIGHT - 60, 180, 40, "ОЧИСТИТЬ", "clear")

        # Кнопки размеров
        self.size_buttons = []
        sizes = [4, 8, 16, 32]
        for i, s in enumerate(sizes):
            rect = pygame.Rect(20 + i*45, SCREEN_HEIGHT - 130, 40, 40)
            self.size_buttons.append((rect, s))

    def set_tool(self, tool_id):
        self.tool = tool_id

    def handle_panel_click(self, pos):
        # Клик по инструментам
        for btn in self.tool_buttons:
            if btn.rect.collidepoint(pos):
                self.set_tool(btn.tool_id)
        
        # Клик по кнопке очистки
        if self.clear_btn.rect.collidepoint(pos):
            self.canvas.fill(WHITE)

        # Клик по палитре (расчет такой же как в main.py)
        palette_y_start = 350
        for i in range(len(PALETTE)):
            row, col = i // 3, i % 3
            rect = pygame.Rect(25 + col * 55, palette_y_start + row * 55, 45, 45)
            if rect.collidepoint(pos):
                self.color = PALETTE[i]

        # Клик по размерам
        for rect, s in self.size_buttons:
            if rect.collidepoint(pos):
                self.brush_size = s

    def mouse_down(self, pos):
        self.drawing = True
        # Координаты клика на холсте (минус ширина тулбара)
        self.start_pos = (pos[0] - TOOLBAR_W, pos[1])

    def mouse_up(self, pos):
        if self.drawing and self.tool in [TOOL_RECT, TOOL_CIRCLE]:
            end_pos = (pos[0] - TOOLBAR_W, pos[1])
            self.draw_shape(self.canvas, self.start_pos, end_pos)
        self.drawing = False

    def mouse_move(self, pos):
        if self.drawing and self.tool in [TOOL_BRUSH, TOOL_ERASER]:
            current_pos = (pos[0] - TOOLBAR_W, pos[1])
            color = WHITE if self.tool == TOOL_ERASER else self.color
            size = self.brush_size * 3 if self.tool == TOOL_ERASER else self.brush_size
            pygame.draw.circle(self.canvas, color, current_pos, size)

    def draw_shape(self, surface, start, end):
        x1, y1 = start
        x2, y2 = end
        rect = pygame.Rect(min(x1, x2), min(y1, y2), abs(x2 - x1), abs(y2 - y1))
        
        if self.tool == TOOL_RECT:
            pygame.draw.rect(surface, self.color, rect, self.brush_size)
        elif self.tool == TOOL_CIRCLE:
            pygame.draw.ellipse(surface, self.color, rect, self.brush_size)