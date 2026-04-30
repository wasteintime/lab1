import pygame
import sys
from racer_entities import *
from persistence import load_settings, save_settings, load_leaderboard, save_score

# UI Colors
DARK_GRAY = (30, 30, 30)
RED = (220, 50, 50)
ROAD_COLOR = (60, 60, 60)
YELLOW = (255, 215, 0)
WHITE = (255, 255, 255)

pygame.init()

class RacerGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Racer Game 🚗")
        self.clock = pygame.time.Clock()
        self.settings = load_settings()
        self.username = "Player"
        self.font_m = pygame.font.SysFont("Arial", 28, bold=True)
        self.font_s = pygame.font.SysFont("Arial", 18)

    def draw_text(self, text, font, color, x, y, center=True):
        img = font.render(text, True, color)
        rect = img.get_rect(center=(x, y)) if center else img.get_rect(topleft=(x, y))
        self.screen.blit(img, rect)

    def main_menu(self):
        name_input = True
        while name_input:
            self.screen.fill(DARK_GRAY)
            self.draw_text("ENTER YOUR NAME:", self.font_m, WHITE, SCREEN_WIDTH//2, 250)
            self.draw_text(self.username + "_", self.font_m, YELLOW, SCREEN_WIDTH//2, 300)
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT: pygame.quit(); sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN: name_input = False
                    elif event.key == pygame.K_BACKSPACE: self.username = self.username[:-1]
                    else: self.username += event.unicode

        while True:
            self.screen.fill(DARK_GRAY)
            self.draw_text("RACER ARCADE", self.font_m, WHITE, SCREEN_WIDTH//2, 100)
            
            buttons = ["PLAY", "SCORES", "SETTINGS", "QUIT"]
            rects = []
            for i, txt in enumerate(buttons):
                r = pygame.Rect(100, 200 + i*60, 200, 45)
                pygame.draw.rect(self.screen, ROAD_COLOR, r, border_radius=10)
                self.draw_text(txt, self.font_m, WHITE, r.centerx, r.centery)
                rects.append((r, txt))

            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT: pygame.quit(); sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for r, txt in rects:
                        if r.collidepoint(event.pos):
                            if txt == "PLAY": self.game_loop()
                            if txt == "SCORES": self.show_leaderboard()
                            if txt == "SETTINGS": self.show_settings()
                            if txt == "QUIT": pygame.quit(); sys.exit()

    def game_loop(self):
        p_color = BLUE if self.settings["color"] == "Blue" else (50, 200, 50) if self.settings["color"] == "Green" else RED
        player = PlayerCar(color=p_color)
        road = RoadMarkings()
        enemies, coins, obstacles, powerups = [], [], [], []
        score, distance, frame_count = 0, 0, 0
        current_speed = 5 if self.settings["diff"] == "Medium" else 3 if self.settings["diff"] == "Easy" else 7
        
        nitro_timer = 0
        running = True
        
        while running:
            self.clock.tick(60)
            frame_count += 1
            dt = pygame.time.get_ticks()
            
            move_speed = current_speed * 2 if player.nitro_active else current_speed
            distance += move_speed / 60
            
            if frame_count % max(30, 80 - int(distance//100)) == 0:
                enemies.append(EnemyCar(move_speed, player.x))
            if frame_count % 120 == 0: obstacles.append(Obstacle())
            if frame_count % 100 == 0: coins.append(Coin())
            if frame_count % 400 == 0: powerups.append(PowerUp())

            for event in pygame.event.get():
                if event.type == pygame.QUIT: pygame.quit(); sys.exit()

            player.move(pygame.key.get_pressed())
            road.update()
            
            if player.nitro_active and dt > nitro_timer:
                player.nitro_active = False

            for e in enemies[:]:
                e.update()
                if e.is_off_screen(): enemies.remove(e)
                if player.get_rect().colliderect(e.get_rect()):
                    if player.shield: player.shield = False; enemies.remove(e)
                    else: running = False

            for c in coins[:]:
                c.update()
                if player.get_rect().colliderect(c.get_rect()):
                    score += c.weight
                    if score % 10 == 0: current_speed += 1
                    coins.remove(c)

            for o in obstacles[:]:
                o.update(move_speed)
                if player.get_rect().colliderect(o.get_rect()):
                    if o.type == "barrier": 
                        if player.shield: player.shield = False
                        else: running = False
                    else: distance -= 10
                    obstacles.remove(o)

            for p in powerups[:]:
                p.update(move_speed)
                if player.get_rect().colliderect(p.get_rect()):
                    if p.type == "nitro": player.nitro_active = True; nitro_timer = dt + 3000
                    elif p.type == "shield": player.shield = True
                    elif p.type == "repair": score += 5
                    powerups.remove(p)

            self.screen.fill((34, 120, 34))
            pygame.draw.rect(self.screen, ROAD_COLOR, (ROAD_LEFT, 0, ROAD_RIGHT - ROAD_LEFT, SCREEN_HEIGHT))
            road.draw(self.screen)
            for x in enemies + coins + obstacles + powerups: x.draw(self.screen)
            player.draw(self.screen)
            
            self.draw_text(f"Очки: {score}  Дист: {int(distance)}m", self.font_s, YELLOW, 10, 10, False)
            if player.nitro_active: self.draw_text("NITRO!", self.font_s, RED, 10, 35, False)
            
            pygame.display.flip()

        save_score(self.username, score, distance)
        self.game_over(score, distance)

    def game_over(self, s, d):
        while True:
            self.screen.fill(BLACK)
            self.draw_text("GAME OVER", self.font_m, RED, SCREEN_WIDTH//2, 200)
            self.draw_text(f"Score: {s}  Distance: {int(d)}m", self.font_s, WHITE, SCREEN_WIDTH//2, 260)
            self.draw_text("Press R to Restart or M for Menu", self.font_s, YELLOW, SCREEN_WIDTH//2, 350)
            pygame.display.flip()
            for e in pygame.event.get():
                if e.type == pygame.QUIT: pygame.quit(); sys.exit()
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_r: self.game_loop()
                    if e.key == pygame.K_m: self.main_menu()

    def show_leaderboard(self):
        while True:
            self.screen.fill(DARK_GRAY)
            self.draw_text("TOP 10 SCORES", self.font_m, YELLOW, SCREEN_WIDTH//2, 50)
            lb = load_leaderboard()
            for i, entry in enumerate(lb):
                txt = f"{i+1}. {entry['name']} - {entry['score']} pts ({entry.get('distance', entry.get('dist', 0))}m)"
                self.draw_text(txt, self.font_s, WHITE, SCREEN_WIDTH//2, 120 + i*35)
            
            self.draw_text("Press ESC to Back", self.font_s, RED, SCREEN_WIDTH//2, 550)
            pygame.display.flip()
            for e in pygame.event.get():
                if e.type == pygame.QUIT: pygame.quit(); sys.exit()
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_ESCAPE: return

    def show_settings(self):
        while True:
            self.screen.fill(DARK_GRAY)
            self.draw_text("SETTINGS", self.font_m, WHITE, SCREEN_WIDTH//2, 100)
            
            opts = [f"Sound: {'ON' if self.settings['sound'] else 'OFF'}", 
                    f"Color: {self.settings['color']}", 
                    f"Diff: {self.settings['diff']}"]
            
            rects = []
            for i, txt in enumerate(opts):
                r = pygame.Rect(80, 200 + i*70, 240, 45)
                pygame.draw.rect(self.screen, ROAD_COLOR, r)
                self.draw_text(txt, self.font_s, WHITE, r.centerx, r.centery)
                rects.append((r, i))

            pygame.display.flip()
            for e in pygame.event.get():
                if e.type == pygame.QUIT: pygame.quit(); sys.exit()
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_ESCAPE: 
                        save_settings(self.settings)
                        return
                if e.type == pygame.MOUSEBUTTONDOWN:
                    for r, idx in rects:
                        if r.collidepoint(e.pos):
                            if idx == 0: self.settings["sound"] = not self.settings["sound"]
                            if idx == 1: 
                                colors = ["Blue", "Green", "Red"]
                                self.settings["color"] = colors[(colors.index(self.settings["color"])+1)%3]
                            if idx == 2:
                                diffs = ["Easy", "Medium", "Hard"]
                                self.settings["diff"] = diffs[(diffs.index(self.settings["diff"])+1)%3]

if __name__ == "__main__":
    game = RacerGame()
    game.main_menu()