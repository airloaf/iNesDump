from iNes import ReadHeader

if __name__ == "__main__":

    # Open up the rom
    rom = open("roms/SuperMarioBros.nes", 'rb')

    # Read the header from the file
    header = ReadHeader(rom)
    print(header)

    # Close the file
    rom.close()