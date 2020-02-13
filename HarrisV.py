import cv2
import numpy as np
 
# Create a VideoCapture object and read from input file.
# If the input is the camera, pass 0 instead of the video file name.

print("Choose from the selected options for Tag videos")
print("press 1 for Tag0")
print("press 2 for Tag1")
print("press 3 for Tag2")
print("press 4 for Multiple_tags")
print("")
I = int(input("Make your selection: "))
if I == 1:
    cap = cv2.VideoCapture('Tag0.mp4')
elif I == 2:
    cap = cv2.VideoCapture('Tag1.mp4')
elif I == 3:
    cap = cv2.VideoCapture('Tag2.mp4')
elif I == 4:
    cap = cv2.VideoCapture('multipleTags.mp4')
else:
    print("Sorry selection could not be identified.")
    exit(0)


if (cap.isOpened()== False): 
  print("Error opening video stream or file")
 
# Read until video is completed
while(cap.isOpened()):
  # Capture frame-by-frame
  ret, frame = cap.read()
  if ret == True:
     gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)  
     dst = cv2.cornerHarris(gray,2,3,0.04)
  
#result is dilated for marking the corners, not important
     dst = cv2.dilate(dst,None)

# Threshold for an optimal value, it may vary depending on the image.
     frame[dst>0.05*dst.max()]=[0,0,255]

  
  # Display the resulting frame
  # Press Q on keyboard to  exit
  if cv2.waitKey(1) & 0xFF == ord('q'):
      break
 
  cv2.imshow('video',frame)
   
# When everything done, release the video capture object.
cap.release()
 
# Closes all the frames
cv2.destroyAllWindows()
