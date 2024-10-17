import random
from PIL import Image, ImageDraw

# Configuration variables
default_width = 250
default_height = 250
default_iterations = 4
default_percent_are_walls = 40
default_output_file = 'noise.png'
default_blob_size = 3  

def generate(width, height, iterations, percentAreWalls):
    map_ = [False] * (width * height)

    randomFill(map_, width, height, percentAreWalls)

    for _ in range(iterations):
        map_ = step(map_, width, height)

    return map_

def randomFill(map_, width, height, percentAreWalls):
    randomColumn = random.randint(4, width - 4)

    for y in range(height):
        for x in range(width):
            if x == 0 or y == 0 or x == width - 1 or y == height - 1:
                map_[x + y * width] = True
            elif x != randomColumn and random.randint(0, 99) < percentAreWalls:
                map_[x + y * width] = True

def step(map_, width, height):
    newMap = [False] * (width * height)

    for y in range(height):
        for x in range(width):
            if x == 0 or y == 0 or x == width - 1 or y == height - 1:
                newMap[x + y * width] = True
            else:
                newMap[x + y * width] = placeWallLogic(map_, width, height, x, y)

    return newMap

def placeWallLogic(map_, width, height, x, y):
    return countAdjacentWalls(map_, width, height, x, y) >= 5 or countNearbyWalls(map_, width, height, x, y) <= 2

def countAdjacentWalls(map_, width, height, x, y):
    walls = 0

    for mapX in range(x - 1, x + 2):
        for mapY in range(y - 1, y + 2):
            if map_[mapX + mapY * width]:
                walls += 1

    return walls

def countNearbyWalls(map_, width, height, x, y):
    walls = 0

    for mapX in range(x - 2, x + 3):
        for mapY in range(y - 2, y + 3):
            if abs(mapX - x) == 2 and abs(mapY - y) == 2:
                continue

            if mapX < 0 or mapY < 0 or mapX >= width or mapY >= height:
                continue

            if map_[mapX + mapY * width]:
                walls += 1

    return walls

def visualizeMap(map_, width, height, outputFile, blobSize):
    image = Image.new('RGBA', (width * blobSize, height * blobSize), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)

    for y in range(height):
        for x in range(width):
            if map_[x + y * width]:
                draw.rectangle((x * blobSize, y * blobSize, (x + 1) * blobSize - 1, (y + 1) * blobSize - 1), fill=(255, 255, 255, 255))

    image.save(outputFile)

# Example usage
if __name__ == "__main__":
    width = default_width
    height = default_height
    iterations = default_iterations
    percentAreWalls = default_percent_are_walls
    outputFile = default_output_file
    blobSize = default_blob_size

    map_ = generate(width, height, iterations, percentAreWalls)
    visualizeMap(map_, width, height, outputFile, blobSize)