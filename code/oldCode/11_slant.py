from os import pathconf_names
from PIL import Image

path_o = '/home/lorenzo/Desktop/font_Arial1_seg0.tif'
path_d = '/home/lorenzo/Desktop/aaa.tif'


def add_border(img, width):
    new = Image.new('RGB', (img.width + 2*width, img.height),(255,255,255))
    new.paste(img, (width, 0))
    return new

def slant(img, sl):
    s = img.transform(img.size, Image.AFFINE, (1, sl, 0,0,1,0))
    return s


img = Image.open(path_o)
img = add_border(img, 30)
img = slant(img, 0.7)

img = img.save(path_d)