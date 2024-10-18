from perlin_noise import PerlinNoise
from config import *
import pygame
import sys
import random

class World():
    def __init__(self, sizeX, sizeY, randomSeed):
        self.generateNoiseMap(sizeX, sizeY, randomSeed)

        flatList = [item for sublist in self.noiseMap for item in sublist]
        self.minValue = min(flatList)
        self.maxValue = max(flatList)

    def generateNoiseMap(self, sizeX, sizeY, randomSeed):
        self.noiseMap = []

        noise1 = PerlinNoise(octaves=3, seed=randomSeed)
        noise2 = PerlinNoise(octaves=6, seed=randomSeed)
        noise3 = PerlinNoise(octaves=12, seed=randomSeed)
        noise4 = PerlinNoise(octaves=24, seed=randomSeed)

        xPix, yPix = sizeX + 1, sizeY + 1
        for j in range(yPix):
            row = []
            for i in range(xPix):
                noiseVal = noise1([i / xPix, j / yPix])
                noiseVal += 0.5 * noise2([i / xPix, j / yPix])
                noiseVal += 0.25 * noise3([i / xPix, j / yPix])
                noiseVal += 0.125 * noise4([i / xPix, j / yPix])
                # noiseVal = random.choice([0,0.5,1])
                row.append(noiseVal)
            self.noiseMap.append(row)
    
    def getTiledMap(self, weights):
        totalWeights = sum(weights)
        totalRange = self.maxValue - self.minValue

        maxTerrainHeights = []
        previousHeight = self.minValue
        for i, terrainType in enumerate(TERRAIN_TYPES):
            height = totalRange * (weights[i] / totalWeights) + previousHeight
            maxTerrainHeights.append(height)
            previousHeight = height
        tiledMap = []

        for row in self.noiseMap:
            mapRow = []
            for value in row:
                terrainType = None
                for i, terrainHeight in enumerate(maxTerrainHeights):
                    if value <= terrainHeight:
                        terrainType = TERRAIN_TYPES[i]
                        break
                if terrainType is None:
                    terrainType = TERRAIN_TYPES[-1]
                mapRow.append(terrainType)

            tiledMap.append(mapRow)

        return tiledMap

class Window:
    def __init__(self, screenPercentage, cellSize):
        pygame.init()
        self.cellSize = cellSize
        self.screenWidth = int(pygame.display.Info().current_w * screenPercentage)
        self.screenHeight = int(self.screenWidth * 9 / 16)
        self.screen = pygame.display.set_mode((self.screenWidth, self.screenHeight))
        self.clock = pygame.time.Clock()
        self.flipPattern = False

    def draw(self, tileMap):
        self.screen.fill((0, 0, 0))
        for i, row in enumerate(tileMap):
            for j, colorID in enumerate(row):
                x = j * (self.cellSize)
                y = i * (self.cellSize)
                if ('dither' in colorID):
                    if ((i+j)%2 == 1):
                        hexColor = TERRAIN_TYPES[int(colorID[-1])]
                    else:
                        hexColor = TERRAIN_TYPES[int(colorID[-2])]
                else:
                    hexColor = colorID

                rgbColor = tuple(int(hexColor[k:k + 2], 16) for k in (1, 3, 5))
                pygame.draw.rect(self.screen, rgbColor, (x, y, self.cellSize, self.cellSize))
        pygame.display.flip()

class EventHandler:
    def __init__(self, window):
        self.window = window

    def handleEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

def main():
    world = World(WORLD_X, WORLD_Y, SEED)
    tileMap = world.getTiledMap(TERRAIN_WEIGHTS)

    window = Window(screenPercentage=WINDOW_SCALING, cellSize=TILESIZE)
    eventHandler = EventHandler(window)

    window.draw(tileMap)

    while True:
        eventHandler.handleEvents()
        window.clock.tick(60)

if __name__ == "__main__":
    main()
