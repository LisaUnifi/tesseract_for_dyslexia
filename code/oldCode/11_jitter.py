import cv2
import numpy as np
from pylab import *

img = cv2.imread('/home/lisa/Desktop/opd1-5.tif')
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # cv2 defaul color code is BGR
h,w,c = img.shape # (768, 1024, 3)

noise = np.random.randint(0,50,(h, w)) # design jitter/noise here
zitter = np.zeros_like(img)
zitter[:,:,1] = noise  

noise_added = cv2.add(img, zitter)
hh = int(h/2)
combined = np.vstack((img[:hh,:,:], noise_added[hh:,:,:]))

#imshow(combined, interpolation='none')
cv2.imwrite('/home/lisa/Desktop/opd1-5.jitter.tif', combined)

#img.save('/home/lisa/Desktop/opd1-5.j.tif', 'TIFF')

