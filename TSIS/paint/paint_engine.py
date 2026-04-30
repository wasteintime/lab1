import pygame
import math
from datetime import datetime

# --- КОНСТАНТЫ ---
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 950
TOOLBAR_W = 220
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PANEL_BG = (55, 55, 60)
DARK_GRAY = (40, 40, 45)
HIGHLIGHT = (0, 120, 215)

# Новые инструменты для TSIS 2
TOOL_PENCIL = "brush" # Это твоя кисть
TOOL_LINE = "line"
TOOL_RECT = "rect"
TOOL_CIRCLE = "circle"
TOOL_ERASER = "eraser"
TOOL_SQUARE = "square"
TOOL_R_TRIANGLE = "r_triangle"
TOOL_E_TRIANGLE = "e_triangle"
TOOL_RHOMBUS = "rhombus"
TOOL_FILL = "fill"
TOOL_TEXT = "text"

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
        self.tool = TOOL_PENCIL
        self.color = BLACK
        self.brush_size = 5
        self.drawing = False
        self.start_pos = None
        self.last_pos = None
        
        # Для текстового инструмента
        self.is_typing = False
        self.text_input = ""
        self.text_pos = (0, 0)

        # Список инструментов (обновлен для TSIS 2)
        tools = [
            ("Карандаш", TOOL_PENCIL), ("Линия", TOOL_LINE),
            ("Ластик", TOOL_ERASER), ("Заливка", TOOL_FILL),
            ("Текст", TOOL_TEXT), ("Прямоуг.", TOOL_RECT),
            ("Круг", TOOL_CIRCLE), ("Квадрат", TOOL_SQUARE),
            ("Ромб", TOOL_RHOMBUS)
        ]
        self.tool_buttons = [Button(20, 70 + i*42, 180, 38, t[0], t[1]) for i, t in enumerate(tools)]
        self.clear_btn = Button(20, SCREEN_HEIGHT - 60, 180, 40, "ОЧИСТИТЬ", "clear")
        self.size_buttons = [(pygame.Rect(25 + i*45, SCREEN_HEIGHT - 130, 35, 35), s) for i, s in enumerate([2, 5, 10])]

    def save_canvas(self):
        filename = datetime.now().strftime("paint_%Y%m%d_%H%M%S.png")
        pygame.image.save(self.canvas, filename)
        print(f"Сохранено как {filename}")

    def flood_fill(self, x, y, new_color):
        """Алгоритм заливки (Stack-based)"""
        target_color = self.canvas.get_at((x, y))
        if target_color == new_color: return
        
        stack = [(x, y)]
        width, height = self.canvas.get_size()

        while stack:
            cx, cy = stack.pop()
            if self.canvas.get_at((cx, cy)) == target_color:
                self.canvas.set_at((cx, cy), new_color)
                if cx > 0: stack.append((cx - 1, cy))
                if cx < width - 1: stack.append((cx + 1, cy))
                if cy > 0: stack.append((cx, cy - 1))
                if cy < height - 1: stack.append((cx, cy + 1))

    def handle_panel_click(self, pos):
        for btn in self.tool_buttons:
            if btn.rect.collidepoint(pos): 
                self.tool = btn.tool_id
                self.is_typing = False # Сброс текста при смене инструмента
        
        if self.clear_btn.rect.collidepoint(pos): self.canvas.fill(WHITE)
        
        palette_y = 460
        for i, color in enumerate(PALETTE):
            r, c = i // 3, i % 3
            if pygame.Rect(25 + c * 55, palette_y + r * 55, 45, 45).collidepoint(pos):
                self.color = color

        for rect, s in self.size_buttons:
            if rect.collidepoint(pos): self.brush_size = s

    def mouse_down(self, pos):
        canvas_x = pos[0] - TOOLBAR_W
        canvas_y = pos[1]
        
        if self.tool == TOOL_FILL:
            self.flood_fill(canvas_x, canvas_y, self.color)
        elif self.tool == TOOL_TEXT:
            self.is_typing = True
            self.text_input = ""
            self.text_pos = (canvas_x, canvas_y)
        else:
            self.drawing = True
            self.start_pos = (canvas_x, canvas_y)
            self.last_pos = self.start_pos

    def mouse_up(self, pos):
        if self.drawing and self.tool not in [TOOL_PENCIL, TOOL_ERASER]:
            end = (pos[0] - TOOLBAR_W, pos[1])
            self.draw_shape(self.canvas, self.start_pos, end, self.brush_size)
        self.drawing = False

    def mouse_move(self, pos):
        if self.drawing and self.tool in [TOOL_PENCIL, TOOL_ERASER]:
            curr = (pos[0] - TOOLBAR_W, pos[1])
            col = WHITE if self.tool == TOOL_ERASER else self.color
            # Для ластика размер чуть больше для удобства
            sz = self.brush_size * 2 if self.tool == TOOL_ERASER else self.brush_size
            pygame.draw.line(self.canvas, col, self.last_pos, curr, sz * 2)
            pygame.draw.circle(self.canvas, col, curr, sz)
            self.last_pos = curr

    def draw_shape(self, target_surface, start, end, size, is_preview=False):
        """Универсальная отрисовка фигур (и на холст, и для превью)"""
        x1, y1 = start
        x2, y2 = end
        dx, dy = x2 - x1, y2 - y1
        color = self.color if not is_preview else (180, 180, 180)

        if self.tool == TOOL_LINE:
            pygame.draw.line(target_surface, color, start, end, size)
        elif self.tool == TOOL_RECT:
            pygame.draw.rect(target_surface, color, (min(x1,x2), min(y1,y2), abs(dx), abs(dy)), size)
        elif self.tool == TOOL_SQUARE:
            side = max(abs(dx), abs(dy))
            sq_x = x1 if dx > 0 else x1 - side
            sq_y = y1 if dy > 0 else y1 - side
            pygame.draw.rect(target_surface, color, (sq_x, sq_y, side, side), size)
        elif self.tool == TOOL_CIRCLE:
            if abs(dx) > 0 and abs(dy) > 0:
                pygame.draw.ellipse(target_surface, color, (min(x1,x2), min(y1,y2), abs(dx), abs(dy)), size)
        elif self.tool == TOOL_R_TRIANGLE:
            pygame.draw.polygon(target_surface, color, [(x1, y1), (x1, y2), (x2, y2)], size)
        elif self.tool == TOOL_E_TRIANGLE:
            pygame.draw.polygon(target_surface, color, [(x1 + dx//2, y1), (x1, y2), (x2, y2)], size)
        elif self.tool == TOOL_RHOMBUS:
            pts = [(x1 + dx//2, y1), (x2, y1 + dy//2), (x1 + dx//2, y2), (x1, y1 + dy//2)]
            pygame.draw.polygon(target_surface, color, pts, size)