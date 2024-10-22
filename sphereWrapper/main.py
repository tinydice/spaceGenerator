from PIL import Image, ImageDraw
import math

PLANET_RADIUS = 150
IMAGE_SIZE = PLANET_RADIUS * 2
OUTPUT_IMAGE_NAME = "planet_image.png"

class Planet:
    def __init__(self, radius):
        self.radius = radius
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

def calculate_theta(x, r):
    y = math.sqrt(r**2 - x**2)
    theta = math.atan2(y, x) * 180 / math.pi
    return theta

planet = Planet(PLANET_RADIUS)
noise = Noise(planet.noiseWrapSize)

image = Image.new("RGB", (IMAGE_SIZE, IMAGE_SIZE), (0, 0, 0))
draw = ImageDraw.Draw(image)

for x in range(IMAGE_SIZE):
    for y in range(IMAGE_SIZE):
        dx = x - planet.radius
        dy = y - planet.radius
        distance = math.sqrt(dx**2 + dy**2)
        if distance <= planet.radius:
            theta = calculate_theta(dx, planet.radius)
            grey_value = int(noise.f(theta) * 255)
            draw.point((x, y), (grey_value, grey_value, grey_value))

image.save(OUTPUT_IMAGE_NAME)
