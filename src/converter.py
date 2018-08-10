from PIL import Image
import numpy as np
from scipy import spatial

ascii_images = {}

"""
Convert an image to binary format and appropriate size for comparison
"""
def convert_to_binary(image):
    image = image.resize((20, 39))
    arr = np.array(image.convert('L'))
    arr[arr < 128] = 0
    arr[arr > 128] = 1
    return arr

"""
Given cw and ch, split an image into cw parts width-wise and ch parts height-wise
"""
def split_image(image, chunks_width, chunks_height):
    image_width = image.size[0]
    image_height = image.size[1]
    w_step = image_width//chunks_width
    h_step = image_height//chunks_height

    current_height = 0
    count_higher = 0
    add_height = 0

    while current_height < image_height:
        current_width = 0
        count_wider = 0
        add_width = 0

        if count_higher < image_height%chunks_height:
            add_height = 1
            count_higher += 1
        elif count_higher == image_height%chunks_height:
            add_height = 0

        while current_width < image_width - 1:
            if count_wider < image_width%chunks_width:
                add_width = 1
                count_wider += 1
            elif count_wider == image_width%chunks_width:
                add_width = 0
            
            #image.crop((current_width, current_height,
            #            current_width + w_step + add_width,
            #            current_height + h_step + add_height)).show()
            yield image.crop((current_width, current_height,
                              current_width + w_step + add_width,
                              current_height + h_step + add_height))
            
            current_width += w_step + add_width
        
        current_height += h_step + add_height


"""
Similarity treating pictures as vectors and calculating the angle between them
"""
# TODO: What about 0 vector?
def cos_similarity(a, b):
    return 1 - spatial.distance.cosine(a.ravel(), b.ravel())

"""
Similarity calculating how many squares have the same colour (value)
"""
# TODO: Black and white shouldn't have the same significance, shape is more important
def binary_similarity(a, b):
    return a.size - np.sum(np.bitwise_xor(a, b).ravel())

"""
Similarity based on how many white (value 1) squares match
"""
# TODO: If a picture is totally white, it will always be the best
def white_similarity(a, b):
    return np.sum((a*b).ravel())

similarity_measures = {
    "binary": binary_similarity,
    "cos": cos_similarity,
    "white": white_similarity
}

def show_binary_image(a):
    Image.frombytes(mode='1', size=a.shape[::-1], data=np.packbits(a, axis=1)).show()

def resize_binary_image(bin_img):
    return Image.frombytes(mode='1', size=a.shape[::-1], data=np.packbits(a, axis=1)).resize((20, 39))

def find_best_match(image, measure="cos"):
    binary_image = convert_to_binary(image)

    best_value = 0
    best_char = " "

    for i in range(32, 127):
        #asc_img = Image.open("../img/" + str(i) + ".png")
        #asc = convert_to_binary(asc_img)
        similarity = similarity_measures[measure](binary_image, ascii_images[i])

        if similarity > best_value:
            best_char = chr(i)
            best_value = similarity
        
        #print("{}: {} similarity {}".format(i, measure, similarity_c))

    #print("Best char: {}".format(best_cos_char))
    
    return best_char

def create_ascii_art(image, width, height, measure="cos", savepath=""):
    result = ""
    widthcount = 0
    for part in split_image(image, width, height):
        result += find_best_match(part, measure)
        widthcount = (widthcount + 1) % width

        if widthcount == 0:
            result += "\n"

    if savepath:
        with open(savepath, "w") as f:
            f.write(result)
    else:
        print(result)

def generate_binary_ascii_images():
    global ascii_images

    for i in range(32, 127):
        img = Image.open("../img/" + str(i) + ".png")
        ascii_images[i] = convert_to_binary(img)


# TODO: For testing
if __name__ == "__main__":
    img = Image.open("/home/mateusz/Pictures/Wallpapers/serpentines.jpg")
    create_ascii_art(img, 40, 20)