import pygame
from src.eventHandler import *

class Window:
    def __init__(self, width, height, title):
        self.width = width
        self.height = height
        self.title = title
        self.window = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(self.title)

    def update(self):
        self.clear()
        self.drawScreen()
        pygame.display.flip()

    def clear(self):
        self.window.fill((0, 0, 0))

    def drawScreen(self):
        pygame.draw.circle(self.window, (255, 0, 0), (250, 250), 50)