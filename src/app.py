from paint import Window
import converter
import sys
from PyQt5.QtWidgets import QApplication
import argparse
from PIL import Image

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", type=str, help="File to convert to ASCII")
    parser.add_argument("-W", "--width", type=int, help="Width of the ASCII art")
    parser.add_argument("-H", "--height", type=int, help="Height of the ASCII art")
    parser.add_argument("-m", "--measure", type=str, help="Measure for the similarity (cos/binary/white)")
    parser.add_argument("-s", "--savepath", type=str, help="Path to save the image in (by default displayed in terminal)")
    args = parser.parse_args()

    if args.file:
        if not args.width or not args.height:
            parser.print_help()
            return
        else:
            converter.generate_binary_ascii_images()

            savepath = args.savepath or ""
            measure = args.measure or "binary"

            converter.create_ascii_art(Image.open(args.file), args.width, args.height, measure, savepath)
            return
    else:
        app = QApplication(sys.argv)
        window = Window()
        sys.exit(app.exec_())

if __name__ == "__main__":
    main()