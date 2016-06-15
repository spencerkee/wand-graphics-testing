from __future__ import division
from PIL import Image
from PIL import ImageDraw
from time import sleep
# from PIL import Display

def myround(x, base):
    return int(base * round(float(x)/base))

def avg(x):
    total = sum(x)
    value = total//3
    return value

def wand_halftone_image(filename, x_res, y_res, shrink_scale):

    orig_im = Image.open(filename)
    width, height = (orig_im.size) #Get the width and hight of the image for iterating over
    new_size = ((int(myround(width, x_res)/shrink_scale)+1), (int(myround(height, y_res)/shrink_scale)+1))#the +1 is so that there is no gap on the right
    orig_im = orig_im.resize(new_size)

    width, height = new_size
    orig_im = orig_im.convert('L')
    orig_matrix = orig_im.load()

    # for x in range(width):
    #     for y in range(height):
            # average = avg(orig_matrix[x,y])
            # orig_matrix[x,y] = (average, average, average)

    new_im = Image.new("RGB", new_size, "white")
    draw_im = ImageDraw.Draw(new_im)
    leftx = 0
    rightx = x_res

    while rightx < width:
        topy = 0
        bottomy = y_res
        while bottomy < height:
            total = 0
            for x in range(leftx,rightx):
                for y in range(topy,bottomy):
                    # total += avg(orig_matrix[x,y])#unecessary, grayscale
                    total += orig_matrix[x,y]

            avg_color  = int(total / (x_res*y_res))
            displacement = avg_color/255
            displacement = 1-displacement
            displacement = displacement * (x_res/2)
            if avg_color != 255:
                draw_im.ellipse((leftx+displacement,topy+displacement,rightx-displacement,bottomy-displacement), fill=(avg_color,avg_color,avg_color,0))
            else:
                print ('found white')
            topy += y_res
            bottomy += y_res
        leftx += x_res
        rightx += x_res

    new_im.show()



if __name__ == '__main__':
    for i in range(5,15):
        wand_halftone_image('flower.jpg', i, i, 1)
        sleep(1)
