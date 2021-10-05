from PIL import Image
  
fg = Image.open('/home/lisa/Desktop/opd1-5.tif')
fg = fg.convert('RGBA')
data = fg.getdata()

newData = []
for i in data:
    if i[0] == 255 and i[1] == 255 and i[2] == 255:
        newData.append((255, 255, 255, 0))
    else:
        newData.append(i)

fg.putdata(newData)
fg.save('/home/lisa/Desktop/opd1-5.fg.tif', 'TIFF')

fg = Image.open('/home/lisa/Desktop/opd1-5.fg.tif')
bg = Image.open('/home/lisa/Desktop/opd1-5.tif')

left = 5
top = 5
w, h = bg.size
newW = w + left
newH = h + top

newBg = Image.new(bg.mode, (newW, newH), (255, 255, 255))
newBg.paste(bg, (left, top))
newBg.save('/home/lisa/Desktop/opd1-5.bg.tif', 'TIFF')

newBg = Image.open('/home/lisa/Desktop/opd1-5.bg.tif')
newBg.paste(fg, (0,0), mask = fg) #starting at coordinate = (0,0)
  
newBg.save('/home/lisa/Desktop/opd1-5.sup.tif', 'TIFF')