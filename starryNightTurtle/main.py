import PIL, random, sys
from PIL import Image, ImageDraw

SIZE = 13
INVADERS = 5
PIXEL_SIZE = 50
PADDING_PIXELS = 1

class InvaderImageGenerator:
    def __init__(self, size, invaders, pixelSize, paddingPixels, colorSeed=None, shapeSeed=None):
        self.size = size
        self.invaders = invaders
        self.pixelSize = pixelSize
        self.paddingPixels = paddingPixels
        self.invaderSize = self.size * self.pixelSize
        self.imgSize = (self.invaders * self.invaderSize) + ((self.invaders + 1) * self.paddingPixels)
        self.listSym = []
        self.colorRng = random.Random(colorSeed) if colorSeed is not None else random.Random()
        self.shapeRng = random.Random(shapeSeed) if shapeSeed is not None else random.Random()
        self.colors = self.generateColors()

    def randomValue(self):
        return self.colorRng.randint(50, 215)

    def randomColor(self):
        return (self.randomValue(), self.randomValue(), self.randomValue())

    def generateColors(self):
        return [self.randomColor(), self.randomColor(), self.randomColor(), (0, 0, 0), (0, 0, 0), (0, 0, 0)]

    def createSquare(self, border, draw, randColor, element):
        if element == int(self.size / 2):
            draw.rectangle(border, fill=randColor)
        elif len(self.listSym) == element + 1:
            draw.rectangle(border, fill=self.listSym.pop())
        else:
            self.listSym.append(randColor)
            draw.rectangle(border, fill=randColor)

    def createInvader(self, border, draw):
        x0, y0, x1, y1 = border
        squareSize = (x1 - x0) / self.size
        i = 1

        for y in range(self.size):
            i *= -1
            element = 0
            for x in range(self.size):
                ulx = x * squareSize + x0
                uly = y * squareSize + y0
                lrx = ulx + squareSize
                lry = uly + squareSize

                self.createSquare((ulx, uly, lrx, lry), draw, self.shapeRng.choice(self.colors), element)

                if element == int(self.size / 2) or element == 0:
                    i *= -1
                element += i

    def generateImage(self):
        origImage = Image.new('RGB', (self.imgSize, self.imgSize))
        draw = ImageDraw.Draw(origImage)

        for x in range(self.invaders):
            for y in range(self.invaders):
                ulx = x * (self.invaderSize + self.paddingPixels) + self.paddingPixels
                uly = y * (self.invaderSize + self.paddingPixels) + self.paddingPixels
                lrx = ulx + self.invaderSize
                lry = uly + self.invaderSize

                shapeSeed = random.random() if not self.shapeRng else self.shapeRng.random()
                self.shapeRng = random.Random(shapeSeed)
                self.createInvader((ulx, uly, lrx, lry), draw)

        origImage.save(f"Ships-{self.size}x{self.size}-{self.invaders}-{self.imgSize}.jpg")

if __name__ == "__main__":
    generator = InvaderImageGenerator(SIZE, INVADERS, PIXEL_SIZE, PADDING_PIXELS, colorSeed=43)
    generator.generateImage()
