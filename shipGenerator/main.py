import PIL, random, sys
from PIL import Image, ImageDraw

ORIG_DIMENSION = 1500
SIZE = 7
INVADERS = 10
IMG_SIZE = 1900

r = lambda: random.randint(50, 215)
rc = lambda: (r(), r(), r())
listSym = []

def create_square(border, draw, randColor, element, size):
    if element == int(size / 2):
        draw.rectangle(border, fill=randColor)
    elif len(listSym) == element + 1:
        draw.rectangle(border, fill=listSym.pop())
    else:
        listSym.append(randColor)
        draw.rectangle(border, fill=randColor)

def create_invader(border, draw, size):
    x0, y0, x1, y1 = border
    squareSize = (x1 - x0) / size
    randColors = [rc(), rc(), rc(), (0, 0, 0), (0, 0, 0), (0, 0, 0)]
    i = 1

    for y in range(0, size):
        i *= -1
        element = 0
        for x in range(0, size):
            topLeftX = x * squareSize + x0
            topLeftY = y * squareSize + y0
            botRightX = topLeftX + squareSize
            botRightY = topLeftY + squareSize

            create_square((topLeftX, topLeftY, botRightX, botRightY), draw, random.choice(randColors), element, size)

            if element == int(size / 2) or element == 0:
                i *= -1
            element += i

def main():
    origDimension = IMG_SIZE
    origImage = Image.new('RGB', (origDimension, origDimension))
    draw = ImageDraw.Draw(origImage)

    invaderSize = origDimension / INVADERS
    padding = invaderSize / SIZE

    for x in range(0, INVADERS):
        for y in range(0, INVADERS):
            topLeftX = x * invaderSize + padding / 2
            topLeftY = y * invaderSize + padding / 2
            botRightX = topLeftX + invaderSize - padding
            botRightY = topLeftY + invaderSize - padding

            create_invader((topLeftX, topLeftY, botRightX, botRightY), draw, SIZE)

    origImage.save("Ships-" + str(SIZE) + "x" + str(SIZE) + "-" + str(INVADERS) + "-" + str(IMG_SIZE) + ".jpg")

if __name__ == "__main__":
    main()
