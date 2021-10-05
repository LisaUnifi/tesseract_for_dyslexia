import cv2

image = cv2.imread('/home/lisa/Desktop/font_OpenDyslexic1_seg13.tif')
blurred = cv2.GaussianBlur(image, (11, 11), 0)
cv2.imwrite('/home/lisa/Desktop/opd1-13.tif', blurred)