from PIL import Image

# Pallette colors to make everything look a bit nicer
palleteColors = [(0, 0, 0), (255, 0, 0), (0, 255, 0), (0, 0, 255)]

def getTile(chrData, tileNumber):
    """ Gets a single tile from the character data.
    """
    tileStart = (tileNumber)*16
    tileEnd = (tileNumber+1)*16

    tileBytes = chrData[tileStart:tileEnd]

    pixels = []

    # For all 8 pixel rows
    for pixelRow in range(8):

        # Get the two bytes of pallette data for each row
        palletteDataLow = tileBytes[pixelRow]
        palletteDataHigh = tileBytes[8+pixelRow]

        # For each pixel in the row
        for pixelNumber in range(8):

            # Calculate the pallete value
            lowBit = (palletteDataLow &0x80) >> 7
            highBit = (palletteDataHigh &0x80) >> 6
            palletteValue = highBit + lowBit

            # Shift the left most bit out
            palletteDataLow = palletteDataLow << 1
            palletteDataHigh = palletteDataHigh << 1

            pixels.append(palletteValue)

    return pixels

def dumpBank(chrBank):
    """ Dumps the given charcater bank into an image.

    Returns a new image with the character bank data
    """
    img = Image.new("RGB", (256, 128), color="black")
    pixels = img.load()

    # Get the first tiles
    for tileRow in range(16):
        for tileCol in range(16):
            tileNumber = tileCol + 16 * tileRow
            tilePixels = getTile(chrBank, tileNumber)

            for pixelRow in range(8):
                for pixelCol in range(8):
                    pixel = pixelRow * 8 + pixelCol
                    pixelColor = palleteColors[tilePixels[pixel]]
                    pixels[tileCol * 8 + pixelCol, tileRow * 8 + pixelRow] = pixelColor

    # Get the 256 tiles
    for tileRow in range(16):
        for tileCol in range(16):
            tileNumber = 255 + tileCol + 16 * tileRow
            tilePixels = getTile(chrBank, tileNumber)

            for pixelRow in range(8):
                for pixelCol in range(8):
                    pixel = pixelRow * 8 + pixelCol
                    pixelColor = palleteColors[tilePixels[pixel]]
                    pixels[128 + tileCol * 8 + pixelCol, tileRow * 8 + pixelRow] = pixelColor

    # Return the image
    return img


def dumpBanks(romData):
    """ Prints character rom to an image

    Arguments:
    romData - the rom data
    """

    # Get the number of banks
    banks = romData["Header"]["CHR_ROM"]

    # List of the banks as images
    bankImages = []

    # For each bank, dump its contents into a png
    for bank in range(banks):
        img = dumpBank(romData['CHR_ROM'][0x2000*bank:0x2000*(bank+1)])
        bankImages.append(img)

    return(bankImages)