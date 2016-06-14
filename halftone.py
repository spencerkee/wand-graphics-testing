from wand.image import Image
from PIL import Image
# from PIL import Display

def myround(x, base):
    return int(base * round(float(x)/base))

def avg(x):
    total = sum(x)
    value = total//3
    return (value,value,value)

def wand_halftone_image(filename, x_res, y_res):

    im = Image.open(filename)
    width, height = (im.size) #Get the width and hight of the image for iterating over
    new_size = (myround(width, x_res), myround(height, y_res))
    im = im.resize(new_size)

    width, height = new_size
    pix_matrix = im.load()
    for x in range(width):
        for y in range(height):
            pix_matrix[x,y] = avg(pix_matrix[x,y])

    im.show()



if __name__ == '__main__':
    wand_halftone_image('original-photo.jpg', 10, 10)
