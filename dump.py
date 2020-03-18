import argparse

from iNes import ReadRom
from CharacterRom import CharacterRomToImage

if __name__ == "__main__":

    # Create argument parser
    parser = argparse.ArgumentParser(description="Dumps an iNes 1.0 file")
    parser.add_argument("-i", "--in-file", metavar="file.nes", type=str, required=True, help="The ines 1.0 file to parse")
    args = parser.parse_args()

    # Read the header from the file
    data = ReadRom(args.in_file)
    print(data['Header'])

    # Export the character rom to an image
    CharacterRomToImage(data)