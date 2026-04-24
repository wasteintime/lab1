import pygame
import sys
from paint_engine import *

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Paint Pro 1200x800")
    clock = pygame.time.Clock()

    app = PaintApp()
    font_btn = pygame.font.SysFont("Arial", 14, bold=True)
    font_title = pygame.font.SysFont("Arial", 18, bold=True)

    while True:
        clock.tick(60)
        mx, my = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if mx < TOOLBAR_W: app.handle_panel_click(event.pos)
                    else: app.mouse_down(event.pos)
            
            if event.type == pygame.MOUSEBUTTONUP:
                app.mouse_up(event.pos)

            if event.type == pygame.MOUSEMOTION:
                app.mouse_move(event.pos)

        # --- ОТРИСОВКА ---
        screen.fill((40, 40, 45))
        screen.blit(app.canvas, (TOOLBAR_W, 0))
        
        # Панель
        pygame.draw.rect(screen, PANEL_BG, (0, 0, TOOLBAR_W, SCREEN_HEIGHT))
        
        title = font_title.render("ИНСТРУМЕНТЫ", True, WHITE)
        screen.blit(title, (TOOLBAR_W//2 - title.get_width()//2, 30))

        # Инструменты
        for btn in app.tool_buttons:
            btn.draw(screen, font_btn, app.tool == btn.tool_id)
        
        # Кнопка очистки
        app.clear_btn.draw(screen, font_btn, False)

        # Палитра
        palette_y = 350
        for i, color in enumerate(PALETTE):
            r, c = i // 3, i % 3
            rect = pygame.Rect(25 + c * 55, palette_y + r * 55, 45, 45)
            pygame.draw.rect(screen, color, rect, border_radius=8)
            if color == app.color:
                pygame.draw.rect(screen, WHITE, rect, 3, border_radius=8)

        # Размеры
        size_txt = font_btn.render("РАЗМЕР КИСТИ:", True, (200, 200, 200))
        screen.blit(size_txt, (20, SCREEN_HEIGHT - 160))
        for rect, s in app.size_buttons:
            bg = HIGHLIGHT if s == app.brush_size else DARK_GRAY
            pygame.draw.rect(screen, bg, rect, border_radius=5)
            pygame.draw.circle(screen, WHITE, rect.center, min(s//2 + 2, 12))

        # Курсор превью
        if mx > TOOLBAR_W:
            r = app.brush_size * 3 if app.tool == TOOL_ERASER else app.brush_size
            pygame.draw.circle(screen, (150, 150, 150), (mx, my), r, 1)

        pygame.display.flip()

if __name__ == "__main__":
    main()