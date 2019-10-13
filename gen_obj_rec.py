# import cv2


# path = 'C:\\Users\\allisony\\AppData\\Local\\Programs\\Python\\Python37-32\\Lib\\site-packages\\~v2\\data'

# faceCascade = cv2.CascadeClassifier(path + '\\haarcascade_frontalface_alt.xml')
# eyeCascade= cv2.CascadeClassifier(path + '\\haarcascade_eye.xml')

# # grab the reference to the webcam
# vs = cv2.VideoCapture(0)

# # keep looping
# while True:
# 	# grab the current frame
# 	ret, frame = vs.read()
  
# 	# if we are viewing a video and we did not grab a frame,
# 	# then we have reached the end of the video
# 	if frame is None:
# 		break
		
# 	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
# 	gray = cv2.equalizeHist(gray)
		
# 	faces = faceCascade.detectMultiScale(frame)

# 	for (x,y,w,h) in faces:
# 		#cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
# 		roi_gray = gray[y:y+h, x:x+w]
# 		roi_color = frame[y:y+h, x:x+w]
# 		eyes = eyeCascade.detectMultiScale(roi_gray)
# 		for (ex,ey,ew,eh) in eyes:
# 			cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
	
# 	# show the frame to our screen
# 	cv2.imshow("Video", frame)
# 	key = cv2.waitKey(1) & 0xFF

# 	# if the 'q' key is pressed, stop the loop
# 	if key == ord("q"):
# 		break
 
# # close all windows
# cv2.destroyAllWindows()

# import cv2


# def canny_webcam():
#     "Live capture frames from webcam and show the canny edge image of the captured frames."

#     cap = cv2.VideoCapture(0)

#     while True:
#         ret, frame = cap.read()  # ret gets a boolean value. True if reading is successful (I think). frame is an
#         # uint8 numpy.ndarray

#         frame = cv2.GaussianBlur(frame, (7, 7), 1.41)
#         frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

#         edge = cv2.Canny(frame, 25, 75)

#         cv2.imshow('Canny Edge', edge)

#         if cv2.waitKey(20) == ord('q'):  # Introduce 20 milisecond delay. press q to exit.
#             break

# canny_webcam()
import cv2
import os
import sys
import numpy as np

def ORB_detector(new_image, image_template):
    # Function that compares input image to template
    # It then returns the number of ORB matches between them
    image1 = cv2.cvtColor(new_image, cv2.COLOR_BGR2GRAY)

    # Create ORB detector with 1000 keypoints with a scaling pyramid factor of 1.2
    orb = cv2.ORB_create(1000, 1.2)

    # Detect keypoints of original image
    (kp1, des1) = orb.detectAndCompute(image1, None)

    # Detect keypoints of rotated image
    (kp2, des2) = orb.detectAndCompute(image_template, None)

    # Create matcher 
    # Note we're no longer using Flannbased matching
    bf = cv2.BFMatcher(cv2.NORM_HAMMING)
    # Do matching
    if des1 is None :
        return False
    if des2 is None :
        return True    
    print('hel')
    matches = bf.match(des1,des2)

    # Sort the matches based on distance.  Least distance
    # is better
    matches = sorted(matches, key=lambda val: val.distance)
    return len(matches)
cap = cv2.VideoCapture(0)


# Load our image template, this is our reference image
print(os.path.isfile('RHEL-python-1569314-pixabay.jpg'))
os.chdir(sys.path[0])
print(os.listdir())
image_template = cv2.imread('./pics/purse.jpeg', cv2.IMREAD_GRAYSCALE) 
print(image_template)
# image_template = cv2.imread('images/kitkat.jpg', 0) 

while True:
    # Get webcam images
    ret, frame = cap.read()

    # Get height and width of webcam frame
    height, width = frame.shape[:2]

    # Define ROI Box Dimensions (Note some of these things should be outside the loop)
    top_left_x = int(width / 3)
    top_left_y = int((height / 2) + (height / 4))
    bottom_right_x = int((width / 3) * 2)
    bottom_right_y = int((height / 2) - (height / 4))

    # Draw rectangular window for our region of interest
    cv2.rectangle(frame, (top_left_x,top_left_y), (bottom_right_x,bottom_right_y), 255, 3)

    # Crop window of observation we defined above
    cropped = frame[bottom_right_y:top_left_y , top_left_x:bottom_right_x]

    # Flip frame orientation horizontally
    frame = cv2.flip(frame,1)

    # Get number of ORB matches 
    matches = ORB_detector(cropped, image_template)

    # Display status string showing the current no. of matches 
    output_string = "Matches = " + str(matches)
    cv2.putText(frame, output_string, (50,450), cv2.FONT_HERSHEY_COMPLEX, 2, (250,0,150), 2)

    # Our threshold to indicate object deteciton
    # For new images or lightening conditions you may need to experiment a bit 
    # Note: The ORB detector to get the top 1000 matches, 350 is essentially a min 35% match
    threshold = 600

    # If matches exceed our threshold then object has been detected
    if matches > threshold:
        cv2.rectangle(frame, (top_left_x,top_left_y), (bottom_right_x,bottom_right_y), (0,255,0), 3)
        cv2.putText(frame,'Object Found',(50,50), cv2.FONT_HERSHEY_COMPLEX, 2 ,(0,255,0), 2)

    cv2.imshow('Object Detector using ORB', frame)
    if cv2.waitKey(1) == 13: #13 is the Enter Key
        break
cap.release()
cv2.destroyAllWindows()