import cv2
import numpy as np

filename = 'ref_marker.png'
Image = cv2.imread(filename)
gray = cv2.cvtColor(Image,cv2.COLOR_BGR2GRAY)
gray = np.float32(gray)
dst = cv2.cornerHarris(gray,6,3,0.04)

#Result is dilated for marking the corners, not important
dst = cv2.dilate(dst,None)

#Threshold for an optimal value, it may vary depending on the image.
Image[dst>0.01*dst.max()]=[0,0,255]

cv2.imshow('Image',Image)
if cv2.waitKey(0) & 0xff == 27:
    cv2.destroyAllWindows()
