import pygame
import sys
from paint_engine import *

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Paint TSIS 2 - Zhanibek")
    clock = pygame.time.Clock()

    app = PaintApp()
    font_btn = pygame.font.SysFont("Arial", 14, bold=True)
    font_text = pygame.font.SysFont("Verdana", 24) # Шрифт для инструмента Текст

    while True:
        clock.tick(60)
        mx, my = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            
            # --- ОБРАБОТКА ТЕКСТА ---
            if app.is_typing:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        # Фиксируем текст на холсте
                        txt_surf = font_text.render(app.text_input, True, app.color)
                        app.canvas.blit(txt_surf, app.text_pos)
                        app.is_typing = False
                    elif event.key == pygame.K_ESCAPE:
                        app.is_typing = False
                    elif event.key == pygame.K_BACKSPACE:
                        app.text_input = app.text_input[:-1]
                    else:
                        app.text_input += event.unicode
                continue # Пока печатаем, другие действия игнорируем

            # --- ОБРАБОТКА МЫШИ ---
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if mx < TOOLBAR_W: app.handle_panel_click(event.pos)
                    else: app.mouse_down(event.pos)
            
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1: app.mouse_up(event.pos)

            if event.type == pygame.MOUSEMOTION:
                app.mouse_move(event.pos)

            # --- ГОРЯЧИЕ КЛАВИШИ ---
            if event.type == pygame.KEYDOWN:
                # Размеры: 1, 2, 3
                if event.key == pygame.K_1: app.brush_size = 2
                if event.key == pygame.K_2: app.brush_size = 5
                if event.key == pygame.K_3: app.brush_size = 10
                
                # Сохранение: Ctrl + S
                if event.key == pygame.K_s and (pygame.key.get_mods() & pygame.KMOD_CTRL):
                    app.save_canvas()

        # --- ОТРИСОВКА ---
        screen.fill((40, 40, 45))
        screen.blit(app.canvas, (TOOLBAR_W, 0))
        
        # LIVE PREVIEW: Рисуем "призрак" фигуры во время перетаскивания
        if app.drawing and app.tool not in [TOOL_PENCIL, TOOL_ERASER]:
            # Создаем временную поверхность для превью, чтобы не пачкать основной экран
            preview_pos = (mx - TOOLBAR_W, my)
            # Рисуем прямо на screen, но со смещением
            app.draw_shape(screen, (app.start_pos[0] + TOOLBAR_W, app.start_pos[1]), (mx, my), app.brush_size, is_preview=True)

        # Отрисовка текста, который вводим прямо сейчас
        if app.is_typing:
            cursor = "|" if pygame.time.get_ticks() % 1000 < 500 else ""
            txt_preview = font_text.render(app.text_input + cursor, True, app.color)
            screen.blit(txt_preview, (app.text_pos[0] + TOOLBAR_W, app.text_pos[1]))

        # Панель
        pygame.draw.rect(screen, PANEL_BG, (0, 0, TOOLBAR_W, SCREEN_HEIGHT))
        for btn in app.tool_buttons:
            btn.draw(screen, font_btn, app.tool == btn.tool_id)
        app.clear_btn.draw(screen, font_btn, False)

        # Палитра
        palette_y = 460 
        for i, color in enumerate(PALETTE):
            r, c = i // 3, i % 3
            rect = pygame.Rect(25 + c * 55, palette_y + r * 55, 45, 45)
            pygame.draw.rect(screen, color, rect, border_radius=8)
            if color == app.color:
                pygame.draw.rect(screen, WHITE, rect, 3, border_radius=8)

        # Размеры
        size_txt = font_btn.render("РАЗМЕР (1, 2, 3):", True, (200, 200, 200))
        screen.blit(size_txt, (20, SCREEN_HEIGHT - 160))
        for rect, s in app.size_buttons:
            bg = HIGHLIGHT if s == app.brush_size else DARK_GRAY
            pygame.draw.rect(screen, bg, rect, border_radius=5)
            pygame.draw.circle(screen, WHITE, rect.center, min(s + 2, 12))

        pygame.display.flip()

if __name__ == "__main__":
    main()