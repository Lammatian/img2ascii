import tkinter as tk
from paint import Paint
import converter
import argparse
from PIL import Image

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", type=str, help="File to convert to ASCII")
    parser.add_argument("-W", "--width", type=int, help="Width of the ASCII art")
    parser.add_argument("-H", "--height", type=int, help="Height of the ASCII art")
    parser.add_argument("-m", "--measure", type=str, help="Measure for the similarity (cos/binary/white)")
    args = parser.parse_args()

    if args.file:
        if not args.width or not args.height:
            parser.print_help()
            return
        else:
            if args.measure:
                converter.create_ascii_art(Image.open(args.file), args.width, args.height, args.measure)
            else:
                converter.create_ascii_art(Image.open(args.file), args.width, args.height)

            return
    else:
        root = tk.Tk()

        app = Paint(root)
        root.mainloop()

if __name__ == "__main__":
    main()