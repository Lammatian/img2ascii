from PIL import Image
import numpy as np
from scipy import spatial

# TODO: Do something about 32.png - zero vector, no similarity!
# TODO: Test different types of similarity
def convert_to_binary(imagepath):
    img = Image.open(imagepath).resize((20, 39))
    arr = np.array(img.convert('L'))
    arr[arr < 128] = 0
    arr[arr > 128] = 1
    return arr

def cos_similarity(a, b):
    return 1 - spatial.distance.cosine(a.ravel(), b.ravel())

def show_binary_image(a):
    Image.frombytes(mode='1', size=a.shape[::-1], data=np.packbits(a, axis=1)).show()

arr = np.random.randint(2, size=(39, 20))
show_binary_image(arr)
best_img = None
best_similarity = 0

for i in range(32, 127):
    asc = convert_to_binary("img/" + str(i) + ".png")
    #arr = convert_to_binary("img/100.png")
    similarity = cos_similarity(asc, arr)

    if similarity > best_similarity:
        best_img = asc
        best_similarity = similarity

    print("{}: similarity {}".format(i, similarity))

show_binary_image(best_img)