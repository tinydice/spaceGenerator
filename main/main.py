import pygame
import sys

class Window:
    def __init__(self, screen_percentage, cell_size, grid_spacing):
        pygame.init()
        self.cell_size = cell_size
        self.grid_spacing = grid_spacing
        self.screen_width = int(pygame.display.Info().current_w * screen_percentage)
        self.screen_height = int(self.screen_width * 9 / 16)
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.clock = pygame.time.Clock()
        self.flip_pattern = False

    def draw_checkerboard(self):
        self.screen.fill((0, 0, 0))
        rows = self.screen_height // (self.cell_size + self.grid_spacing)
        cols = self.screen_width // (self.cell_size + self.grid_spacing)
        for row in range(rows):
            for col in range(cols):
                if (row + col + self.flip_pattern) % 2 == 0:
                    x = col * (self.cell_size + self.grid_spacing)
                    y = row * (self.cell_size + self.grid_spacing)
                    pygame.draw.rect(self.screen, (255, 255, 255), (x, y, self.cell_size, self.cell_size))
        pygame.display.flip()

class EventHandler:
    def __init__(self, window):
        self.window = window

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.window.flip_pattern = not self.window.flip_pattern
                self.window.draw_checkerboard()

def main():
    window = Window(screen_percentage=0.8, cell_size=20, grid_spacing=2)
    event_handler = EventHandler(window)

    window.draw_checkerboard()

    while True:
        event_handler.handle_events()
        window.clock.tick(60)



if __name__ == "__main__":
    main()

