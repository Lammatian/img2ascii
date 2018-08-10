from PIL import Image
import numpy as np
from scipy import spatial

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

def show_binary_image(a):
    Image.frombytes(mode='1', size=a.shape[::-1], data=np.packbits(a, axis=1)).show()

def resize_binary_image(bin_img):
    return Image.frombytes(mode='1', size=a.shape[::-1], data=np.packbits(a, axis=1)).resize((20, 39))

def find_best_match(image):
    binary_image = convert_to_binary(image)

    best_match_cos = None
    best_similarity_cos = 0
    best_cos_char = " "

    for i in range(32, 127):
        asc_img = Image.open("../img/" + str(i) + ".png")
        asc = convert_to_binary(asc_img)
        similarity_c = cos_similarity(asc, binary_image)

        if similarity_c > best_similarity_cos:
            best_cos_char = chr(i)
            best_match_cos = asc
            best_similarity_cos = similarity_c
        
        #print("{}: cosine similarity {}".format(i, similarity_c))

    #print("Best char: {}".format(best_cos_char))
    
    return best_cos_char

def create_ascii_art(image, width, height):
    result = ""
    widthcount = 0
    for part in split_image(image, width, height):
        result += find_best_match(part)
        widthcount = (widthcount + 1) % width

        if widthcount == 0:
            result += "\n"

    return result

if __name__ == "__main__":
    img = Image.open("/home/mateusz/Pictures/Wallpapers/serpentines.jpg")

    print(create_ascii_art(img, 40, 40))