"""
*****************  Team Members: PRASANNA MARUDHU BALASUBRAMANIAN (116197700) , SAKET SESHADRI GUDIMETLA (116332293), CHAYAN KUMAR PATODI (116327428)

*****************  Class: Robotics - 2019 Spring Semester    ********************
*****************  Course: ENPM673-Perception for Autonomous Robots   ********************
###
 
* This Python program is developed to Detect the AR Tag, Find the Edges and Contours of Tag, Superimpose the Lena Image onto the Tag and to Draw a cube on the AR tag *

###

"""

### Modules used in the program
import cv2
import Image
import PIL
from PIL import Image
import os
from ID_SubFunctions import *
from ID_PatternCheck import *

###Capturing the frames of the given video using the VideoCapture function
###by accepting the input from the user
print("Select anyone of the Tag videos below : ")
print("press 1 for Tag0")
print("press 2 for Tag1")
print("press 3 for Tag2")
print("press 4 for Multiple_tags")
print("")

option = int(input("Make your selection: "))
if option == 1:
    cap = cv2.VideoCapture('Tag0.mp4')
elif option == 2:
    cap = cv2.VideoCapture('Tag1.mp4')
elif option == 3:
    cap = cv2.VideoCapture('Tag2.mp4')
elif option == 4:
    cap = cv2.VideoCapture('multipleTags.mp4')
else:
    print("The option you selected doesnot exists, stopping the execution")
    exit(0)


###Checking whether it is possible to open the video and if not then the error message is displayed
if (cap.isOpened()== False): 
    print("Error opening video stream or file") 	#Error message printing

###Initializing the variables with values that to be used in the program
Corner_points = 4               #Number of image corners
Threshold_BlackColor = 100    	#Black threshold limit vale
SHAPE_RESIZE = 100.0
Threshold_WhiteColor = 155	#White threshold limit vale

while True:
 
    ### Checking if the camera is opened successfully
    ### Reading until video is completed
    if (cap.isOpened()==True):
    ### Capture each frame in the video
        ret, image = cap.read()
   
 
### Detecting the given AR_Tag:
    ### Converting the image to Gray
    Gray_Img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    ###Smoothening the image using 'GaussianBlur' function
    Gray_Img = cv2.GaussianBlur(Gray_Img, (5,5), 0)
    ###Detecting the edges of the image using 'Canny' edge detector
    Detect_Edge = cv2.Canny(Gray_Img, 100, 250)
        
    ###Determining the Tag contours using the 'findContours' function
    _, contours, _ = cv2.findContours(Detect_Edge, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE) 
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]
    #cv2.drawContours(image,contours,-1,(15,255,155),2)

    #Obtaining the ID Tag pattern

    for contour in contours:
   
        # Contour Approximation-It approximates a contour shape to another shape with less number of vertices depending upon the precision we specify
        Contour_Perim = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.01*Contour_Perim, True)

        if len(approx) == Corner_points:
            
            # Perspective warping function is carried out by calling 'Normal_OrientTrans'function
            Orient_Img = Normal_OrientTrans(Gray_Img, approx.reshape(4,2))
            #Resizing the image                 
            Img_Resize = cv2.resize(Orient_Img, (390,390))     
            #Converting the image to binary image with pixel threshold
            BW_Img = cv2.threshold(Img_Resize,250 ,255, cv2.THRESH_BINARY)[1]     
            
	    #Obtaining the AR tag ID data decimal value through the Obtain_TagID function      
	    AR_Id=Obtain_TagID(BW_Img, Threshold_BlackColor, Threshold_WhiteColor)
	    
            # Deriving the binary ID tag value along with the orientation id with black and white image
            Binary_ID = Binary_ID_Val(BW_Img, Threshold_BlackColor, Threshold_WhiteColor)
             
	    #Calculating the number of rotation required to super impose the Lena image, existence of the ID tag and orientation to substitute the image on the tag through
            #Compare Binary ID function  
            IDTag_Recog, Count_Rot, Repl_TagVal = Compare_Binary_ID(Binary_ID)

            #when the ID is recognized then the Lena image is read and superimposed onto the AR Tag
            if IDTag_Recog:
 
                # Stage 8: Substitute glyph
                Lena_Repl_Img = cv2.imread('Lena.png'.format(Repl_TagVal))
            	#Based on the obtained orientation of the AR Tag, the Lena image is superimposed     
                for _ in range(Count_Rot):
                    Lena_Repl_Img = LenaImg_Angle_shift(Lena_Repl_Img, -90)
                
                image = SuperImposeImg(image, Lena_Repl_Img, approx.reshape(4, 2))
		#Obtainng the homography matrix
		A= Normal_OrientTrans2(Gray_Img, approx.reshape(4,2))
		#Writing the Tag ID on the image		
		font=cv2.FONT_HERSHEY_SIMPLEX
		cv2.putText(image,("Tag ID is : "+str(AR_Id)),(100,140),font, 1,(0,255,0),2,cv2.LINE_AA)      
		#Display Output          
		cv2.imshow('Output', image)

                # Stage 9: Add effects
                image = CubeSubs_Img(A, image, approx.reshape(4, 2))
                       
    #cv2.imshow('AR Tag Detection and Effects', image)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the video capture object
#cap.release()
 
# Closes all the frames
cv2.destroyAllWindows()
