from PIL import Image, ImageFilter
import numpy as np
import os

Image.MAX_IMAGE_PIXELS = None  # позволяет окрывать изображения большого размера


def split_image(path, input, length):
    im = Image.open(input)
    imgwidth, imgheight = im.size
    row = column = 1
    for i in range(0, imgheight//length*length, length):
        for j in range(0, imgwidth//length*length, length):
            box = (j, i, j+length, i+length)
            a = im.crop(box)
            a.save(path + str(row) + "_" + str(column) + ".tif")
            column += 1
        column = 1
        row += 1


def remove_images_without_tissue(path):
    with os.scandir(path) as entries:
        for entry in entries:
            im = Image.open(path + entry.name)
            im_array_reshape = np.reshape(np.array(im), (16384, 3))
            im_array_unique = np.unique(im_array_reshape, axis=0)
            if im_array_unique.__len__() < 1500:
                os.remove(path + entry.name)


list = [4]  # номера изображений из директории ./images/source для обработки
#  нарезка изображений на патчи размера 128x128
for i in list:
    split_image("./images/split_images/{}/".format(i), "./images/source/{}.tif".format(i), 128)


#  удаление изображений 128х128 без тканей
for i in list:
    remove_images_without_tissue('./images/split_images/{}/'.format(i))