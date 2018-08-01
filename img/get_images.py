from os import system, path
import pyscreenshot as pysc
from PIL import Image
from time import sleep

# Get images of all ASCII characters
# Works only on Linux (system("clear"))
# Assumes font 72 and full-screen terminal
# Probably doesn't work in different resolutions than mine

# Turn off cursor
system("setterm -cursor off")

# Grab screenshots of all ASCII characters between 32 and 127 and crop them out
for i in range(32, 127):
    system("clear")
    print(chr(i))
    # Screen seems to be grabbed before print happens, that's why we need sleep (lol)
    sleep(0.05)
    image = pysc.grab()
    # (left, top, right, bottom)
    image = image.crop((0, 34, 80, 190))
    image.save(str(i) + ".png")

# Turn cursor back on
system("setterm -cursor on")