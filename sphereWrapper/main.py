import math
import pygame

class Planet:
    def __init__(self, radius):
        self.px = 1
        self.radius = radius * self.px
        
        self.area = math.pi * (self.radius) ** 2
        self.circumference = 2 * math.pi * self.radius
        self.noiseWrapSize = self.circumference

class Noise:
    def __init__(self, maxVal):
        self.maxVal = maxVal

    def f(self, theta):
        if self.maxVal == 0:
            return 0
        
        return (theta / 180) ** 2

class Window:
    def __init__(self, width, height, title):
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption(title)

    def fill(self, color):
        self.screen.fill(color)

    def draw_circle(self, color, center, radius):
        pygame.draw.circle(self.screen, color, center, radius)

    def update(self):
        pygame.display.flip()

class EventHandler:
    def __init__(self):
        self.running = True

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

def calculate_theta(x, r):
    if x < -r or x > r:
        raise ValueError("x must be between -r and r for the half-circle")

    y = math.sqrt(r**2 - x**2)
    theta = math.atan2(y, x) * 180 / math.pi
    return theta

planet = Planet(200)
noise = Noise(planet.noiseWrapSize)

planet_window = Window(int(planet.radius * 2), int(planet.radius * 2), "Planet View")
planet_window.fill((0, 0, 0))

for x in range(int(planet.radius * 2)):
    for y in range(int(planet.radius * 2)):
        dx = x - planet.radius
        dy = y - planet.radius
        distance = math.sqrt(dx**2 + dy**2)
        if distance <= planet.radius:
            theta = calculate_theta(dx, planet.radius)
            grey_value = int(noise.f(theta) * 255)
            planet_window.screen.set_at((x, y), (grey_value, grey_value, grey_value))

planet_window.update()

event_handler = EventHandler()
while event_handler.running:
    event_handler.handle_events()
