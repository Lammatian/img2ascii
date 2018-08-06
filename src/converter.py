from PIL import Image
import numpy as np
from scipy import spatial

def convert_to_binary(imagepath):
    img = Image.open(imagepath).resize((20, 39))
    arr = np.array(img.convert('L'))
    arr[arr < 128] = 0
    arr[arr > 128] = 1
    return arr

def split_image(binary_image, chunks_width, chunks_height):
    w_step = binary_image.shape[1]//chunks_width
    h_step = binary_image.shape[0]//chunks_height
    print(w_step, h_step)

    current_width = 0
    count_wider = 0
    add_width = 0

    while current_width < binary_image.shape[1]:
        current_height = 0
        count_higher = 0
        add_height = 0

        if count_wider < binary_image.shape[1]%chunks_width:
            add_width = 1
            count_wider += 1
        elif count_wider == binary_image.shape[1]%chunks_width:
            add_width = 0

        while current_height < binary_image.shape[0] - 1:
            if count_higher < binary_image.shape[0]%chunks_height:
                add_height = 1
                count_higher += 1
            elif count_higher == binary_image.shape[0]%chunks_height:
                add_height = 0
            
            print((current_height, current_height + h_step + add_height))
            print((current_width, current_width + w_step + add_width))
            print(binary_image[current_height:(current_height + h_step + add_height),
                               current_width:(current_width + w_step + add_width)])
            
            current_height += h_step + add_height
        
        current_width += w_step + add_width


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

def find_best_match(imagepath):
    binary_image = convert_to_binary(imagepath)

    best_match_binary = None
    best_similarity_binary = 0
    best_match_cos = None
    best_similarity_cos = 0

    for i in range(32, 127):
        asc = convert_to_binary("img/" + str(i) + ".png")
        similarity_c = cos_similarity(asc, binary_image)
        similarity_b = binary_similarity(asc, binary_image)

        if similarity_c > best_similarity_cos:
            best_match_cos = asc
            best_similarity_cos = similarity_c
        if similarity_b > best_similarity_binary:
            best_match_binary = asc 
            best_similarity_binary = similarity_b
        
        print("{}: cosine similarity {} | binary similarity {}".format(i, similarity_c, similarity_b))
    
    show_binary_image(best_match_cos)
    show_binary_image(best_match_binary)
    return best_match_cos

if __name__ == "__main__":
    print(convert_to_binary("../img/100.png"))
    split_image(convert_to_binary("../img/100.png"), 3, 3)