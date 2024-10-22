import PIL, random, sys
from PIL import Image, ImageDraw

class invaderImageGenerator:
    def __init__(self, pixelSize, invaders, size, shipSeed=None, shipIndex=None, colorSeed=None, colorIndex=None):
        self.size = size
        self.invaders = invaders
        self.pixelSize = pixelSize
        self.imgSize = self.invaders * self.size * self.pixelSize + self.pixelSize
        self.listSym = []
        self.shipSeed = int(shipSeed) if shipSeed is not None else int(random.random() * 10000)
        self.shipIndex = shipIndex
        self.colorSeed = int(colorSeed) if colorSeed is not None else int(random.random() * 10000)
        self.colorIndex = colorIndex
        print(f'shipSeed = {self.shipSeed}, colorSeed = {self.colorSeed}') 

    def randomValue(self):
        return self.colorRNG.randint(50, 215)

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

    def drawInvader(self, index, border, draw):
        x0, y0, x1, y1 = border
        squareSize = (x1 - x0) / self.size
        i = 1
        
        if (self.shipIndex is not None):
            shipOffset = self.shipIndex
        else:
            shipOffset = index 

        if (self.colorIndex is not None):
            colorOffset = self.colorIndex
        else:
            colorOffset = index

        self.shipRNG = random.Random(self.shipSeed+shipOffset)
        self.colorRNG = random.Random(self.colorSeed+colorOffset)
        self.colors = self.generateColors()

        for y in range(self.size):
            i *= -1
            element = 0
            for x in range(self.size):
                ulx = x * squareSize + x0
                uly = y * squareSize + y0
                lrx = ulx + squareSize
                lry = uly + squareSize

                squareColor = self.shipRNG.choice(self.colors)

                self.createSquare((ulx, uly, lrx, lry), draw, squareColor, element)

                if element == int(self.size / 2) or element == 0:
                    i *= -1
                element += i

    def generateImage(self):
        origImage = Image.new('RGB', (self.imgSize, self.imgSize))
        draw = ImageDraw.Draw(origImage)

        invaderSize = self.imgSize / self.invaders
        padding = invaderSize / self.size
        invaderIndex = 0
        for x in range(self.invaders):        
            for y in range(self.invaders):
                ulx = x * invaderSize + padding / 2
                uly = y * invaderSize + padding / 2
                lrx = ulx + invaderSize - padding
                lry = uly + invaderSize - padding

                self.drawInvader(invaderIndex, (ulx, uly, lrx, lry), draw)

                invaderIndex += 1

        origImage.save(f"Ships-{self.invaders}x{self.invaders}.jpg")

if __name__ == "__main__":
    pixelSize=50
    invaders=10
    size=7

    shipSeed = 9048
    shipIndex = 41
    colorSeed = 5306
    colorIndex = 41
    generator = invaderImageGenerator(pixelSize=pixelSize, invaders=invaders, size=size, shipSeed=shipSeed, shipIndex=shipIndex, colorSeed=colorSeed, colorIndex=colorIndex)
    generator = invaderImageGenerator(pixelSize=pixelSize, invaders=invaders, size=size, colorSeed=colorSeed, colorIndex=colorIndex)
    #generator = invaderImageGenerator(pixelSize=pixelSize, invaders=invaders, size=size, shipSeed=shipSeed, colorSeed=colorSeed)
    #generator = invaderImageGenerator(pixelSize=pixelSize, invaders=invaders, size=size)

    generator.generateImage()



# ' shipSeed=58 is cute af