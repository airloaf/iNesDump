from PIL import Image

palleteColors = [(0, 0, 0), (255, 0, 0), (0, 255, 0), (0, 0, 255)]

def getTile(chrData, tileNumber):
    """ Get the tile from the charcater data
    """
    tileStart = (tileNumber)*16
    tileEnd = (tileNumber+1)*16

    tileBytes =chrData[tileStart:tileEnd]

    pixels = []

    # For all 8 pixel rows
    for pixelRow in range(8):

        # Get the two bytes of pallete data for each row
        palleteDataLow = tileBytes[pixelRow]
        palleteDataHigh = tileBytes[8+pixelRow]

        # For each pixel in the row
        for pixelNumber in range(8):

            # Calculate the pallete value
            lowBit = (palleteDataLow &0x80) >> 7
            highBit = (palleteDataHigh &0x80) >> 6
            palleteValue = highBit + lowBit

            # Shift the left most bit out
            palleteDataLow = palleteDataLow << 1
            palleteDataHigh = palleteDataHigh << 1

            pixels.append(palleteValue)

    return pixels

def CharacterRomToImage(romData):
    """ Prints character rom to an image

    Arguments:
    romData - the rom data
    """

    img = Image.new("RGB", (256, 128), color="black")
    pixels = img.load()

    # Get the first tiles
    for tileRow in range(16):
        for tileCol in range(16):
            tileNumber = tileCol + 16 * tileRow
            tilePixels = getTile(romData['CHR_ROM'], tileNumber)

            for pixelRow in range(8):
                for pixelCol in range(8):
                    pixel = pixelRow * 8 + pixelCol
                    pixelColor = palleteColors[tilePixels[pixel]]
                    pixels[tileCol * 8 + pixelCol, tileRow * 8 + pixelRow] = pixelColor

    # Get the 256 tiles
    for tileRow in range(16):
        for tileCol in range(16):
            tileNumber = 255 + tileCol + 16 * tileRow
            tilePixels = getTile(romData['CHR_ROM'], tileNumber)

            for pixelRow in range(8):
                for pixelCol in range(8):
                    pixel = pixelRow * 8 + pixelCol
                    pixelColor = palleteColors[tilePixels[pixel]]
                    pixels[128 + tileCol * 8 + pixelCol, tileRow * 8 + pixelRow] = pixelColor

    img.save('test.png')
    pass