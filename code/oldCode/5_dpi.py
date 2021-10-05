from PIL import Image
import os 

path = 'C:/Users/lisac/Desktop/MarinaiProgetto/dpi/'
dir = 'Verdana'
for file in os.listdir(path + dir):
    if file.endswith('.tif'):
        print(file)
        img = Image.open(path + dir + '/' + file)
        exif_data = img.getexif()
        dict(exif_data)
        #print(exif_data)
        img.save(path + dir + '/' + file, dpi=(300.0, 300.0))

        img = Image.open(path + dir + '/' + file)
        exif_data = img.getexif()
        dict(exif_data)
        print(exif_data)

