import cv2
import numpy as np
from ID_Cube import Effects   #Calling the Effects class from the effects file
 
effects = Effects()



#Function to obtaint the Tag ID to be printed on the video frame
def Obtain_TagID(image, Threshold_BlackColor, Threshold_WhiteColor):
    
    #Resizing the image
    im2 = image[146:2243,146:243]     #[146:243,146:243]

    #Calculate ID
    ret_val = 0
    a=0
    b=0
    binary=[]
    ret_val = 0
    count = 0
    val=0
    
    for i in range(2):        
        for y in (1,2):            
            a=(i+1)*42
            b=42*y
            px2 = im2[a,b]  #y* width + width/2
            
            if px2 >= Threshold_WhiteColor:
                val = 1
                binary.append(val)
            else:
                val = 0
                binary.append(val)

            ret_val+= val*pow(2, count)
            count+=1

    #Tag ID value is returned
    return ret_val

#Function which rotates the Lena image and return to main function to superimpose on the AR Tag
def LenaImg_Angle_shift(image, angle):
    (h, w) = image.shape[:2]
    center = (w / 2, h / 2)
    matrix_rot = cv2.getRotationMatrix2D(center, angle, 1.0)
    return cv2.warpAffine(image, matrix_rot, (w, h))


#Function to obtain the max height and width of the image
def Normal_OrientPts(max_width, max_height):
    return np.array([
        [0, 0],
        [max_width-1, 0],
        [max_width-1, max_height-1],
        [0, max_height-1]], dtype="float32")
 
#Function calls for the obtinaing the Cube over the Tag 
def CubeSubs_Img(A, image, pts_val):
     
    # order points
    pts_val = PointsDetection(pts_val)
 
    # add cube effect
    image = effects.tag_cube(A, image, pts_val)
 
    return image

#This functions helps in obtaining the warped image on the tag
def Normal_OrientTrans(image, source_pts):
 
    # source_pts and destination points
    source_pts = PointsDetection(source_pts)
    #Determing the max height and width of the image through source points 
    (max_width,max_height) = Dimension_hw_max(source_pts)
    destin_pts = Normal_OrientPts(max_width, max_height) # Determining the destination points through 'Normal_OrientPts'
  
    # Homography matrix obtained through the cv2 getPerspectiveTransform function
    homography_matrix = cv2.getPerspectiveTransform(source_pts, destin_pts)
    #Warping the image through warpPerspective function
    Img_Transwarped = cv2.warpPerspective(image, homography_matrix, Dimension_hw_max(source_pts))
 
    # returning the warped image
    return Img_Transwarped


#This function returns the homography matrix to calculate the rotational and translation vectors
def Normal_OrientTrans2(image, source_pts):
 
    # source_pts and destination points
    source_pts = PointsDetection(source_pts)
 
    (max_width,max_height) = Dimension_hw_max(source_pts)
    destin_pts = Normal_OrientPts(max_width, max_height)
  
    # Homography matrix obtained through the cv2 getPerspectiveTransform function
    homography_matrix = cv2.getPerspectiveTransform(source_pts, destin_pts)
    #Warping the image through warpPerspective function
    Img_Transwarped = cv2.warpPerspective(image, homography_matrix, Dimension_hw_max(source_pts))
 
    # return the homography matrix
    return homography_matrix

#This function determines the image width and height and warp the subsitute image  
def SuperImposeImg(image, Lena_Repl_Img, destin_pts):
 
    # dst (zeroed) and src points
    destin_pts = PointsDetection(destin_pts)
 
    (tl, tr, br, bl) = destin_pts
    min_x = min(int(tl[0]), int(bl[0]))
    min_y = min(int(tl[1]), int(tr[1]))
 
    for point in destin_pts:
        point[0] = point[0] - min_x
        point[1] = point[1] - min_y
 
    (max_width,max_height) = Dimension_hw_max(destin_pts)
    source_pts = Normal_OrientPts(max_width, max_height)
 
    # warp perspective (with white border)
    Lena_Repl_Img = cv2.resize(Lena_Repl_Img, (max_width,max_height))
 
    Img_Transwarped = np.zeros((max_height,max_width,3), np.uint8)
    Img_Transwarped[:,:,:] = 255
 
    homography_matrix = cv2.getPerspectiveTransform(source_pts, destin_pts)
    cv2.warpPerspective(Lena_Repl_Img, homography_matrix, (max_width,max_height), Img_Transwarped, borderMode=cv2.BORDER_TRANSPARENT)
 
    # add substitute quad
    image[min_y:min_y + max_height, min_x:min_x + max_width] = Img_Transwarped
 
    return image

#Detecting the points and ordered
def PointsDetection(pts_val):
 
    s = pts_val.sum(axis=1)
    diff = np.diff(pts_val, axis=1)
     
    pts_arr = np.zeros((4,2), dtype="float32")
 
    pts_arr[0] = pts_val[np.argmin(s)]
    pts_arr[2] = pts_val[np.argmax(s)]
    pts_arr[1] = pts_val[np.argmin(diff)]
    pts_arr[3] = pts_val[np.argmax(diff)]
 
    return pts_arr
  
#The orientation pattern of the AR Tag through calculating the binary value of orientation pattern
def Binary_ID_Val(image, black_threshold, white_threshold):
    
    im = image[95:290,95:290]     #[98:293,98:293]
    
    #Calculate ID
    ret_val = 0
    val=0
    binary=[]
    ret_val = 0
    count = 0
    a=0
    b=0

    for i in range(4):        
        for y in (1,2,3,4):            
            a=(i+1)*42
            b=42*y
            px1 = im[a,b]  #y* width + width/2
            
            if px1 >= white_threshold:
                val = 1
                binary.append(val)
            else:
                val = 0
                binary.append(val)

            ret_val+= val*pow(2, count)
            count+=1

    return binary

#This function helps in determingn the max height and width of the image at a particular frame
def Dimension_hw_max(pts_val):
 
    (tl, tr, br, bl) = pts_val
 
    top_width = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
    bottom_width = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
    max_width =( max(int(top_width), int(bottom_width)) )
 
    left_height = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
    right_height = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
    max_height =( max(int(left_height), int(right_height)) )
 
    return (max_width,max_height)


 
