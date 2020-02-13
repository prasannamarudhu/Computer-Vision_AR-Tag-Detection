#Modules used in this program
import cv2
import numpy as np
import glob
import numpy as np
import cv2
from matplotlib import pyplot as plt
import copy
import math
import time
from numpy.linalg import inv
from numpy.linalg import norm

#This class contributes in calcualtinig the rotation, tanslation vectors and projective points through below mentioned functions
class Effects:

    # This function calculates the rotation, tanslation vectors with hekpl of homography matrix
    def calculate(self,h):
        K = np.array([[1406.08415449821, 0, 0], [2.20679787308599, 1417.99930662800, 0], [1014.13643417416, 566.347754321696, 1]]).T
        h = inv(h)
        b_new = np.dot(inv(K), h)
        b1 = b_new[:, 0].reshape(3, 1)
        b2 = b_new[:, 1].reshape(3, 1)
        r3 = np.cross(b_new[:, 0], b_new[:, 1])
        b3 = b_new[:, 2].reshape(3, 1)
        L = 2 / (norm((inv(K)).dot(b1)) + norm((inv(K)).dot(b2)))
        r1 = L * b1
        r2 = L * b2
        r3 = (r3 * L * L).reshape(3, 1)
        t = L * b3
        r = np.concatenate((r1, r2, r3), axis=1)

        return r, t, K

    #This function helps in determing the projective points through the 'projectPoints' function
    def tag_cube(self, A, image, points):
	

        axis = np.float32([[0, 0, 0], [0, 200, 0], [200, 200, 0], [200, 0, 0], [0, 0, -200], [0, 200, -200], [200, 200, -200],[200, 0, -200]])
        H_matrix = A
        dist = np.zeros((1, 5))
	r, t, K = self.calculate(H_matrix)
        imgpts, _ = cv2.projectPoints(axis, r, t, K, dist)
	

        self._draw_cube(image, imgpts)
        #cv2.imshow('img',image)
        return image

		
    #This function draws the cube onto the tag with pillars, base and roof
    def _draw_cube(self, image, imgpts):
	
        imgpts = np.int32(imgpts).reshape(-1,2)
                
        image = cv2.drawContours(image, [imgpts[:4]],-1,(0,0,255),3)
	
        # Drawing the pillars in green color
        for i,j in zip(range(4),range(4,8)):
            cv2.line(image,tuple(imgpts[i]),tuple(imgpts[j]),(0,255,0),4)
        
        # Drawing the upper roof in red
        cv2.drawContours(image, [imgpts[4:]],-1,(255,0,0),3)
        
	return image
	
