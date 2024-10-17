import pygame
from src.eventHandler import *
from src.window import *

class App:
    def __init__(self):
        pygame.init()
        self.window = Window(500, 500, "Pixel Art Generator")
        self.eventHandler = eventHandler()
        self.running = True

    def run(self):
        while self.running:
            self.eventHandler.handleEvents()
            self.window.update()