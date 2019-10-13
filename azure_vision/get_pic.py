import cv2
import pyttsx3
import time
cam = cv2.VideoCapture(0)
cv2.namedWindow("test")
engine = pyttsx3.init()


def display_vid(cam,engine):
	img_counter = 0
	pics = 0
	while True:
		img_counter += 1
		ret, frame = cam.read()
		cv2.imshow("test", frame)
		if( img_counter > 100):
			if( img_counter %30 == 0):
				pics += 1
				engine.say("snap")
				engine.runAndWait()
				time.sleep(0.75)
				cv2.imwrite("./frame%d.jpg" % pics, frame)
		k = cv2.waitKey(1)
		if k%256 == 27:
		# ESC pressed
			print("Escape hit, closing...")
			break
display_vid(cam,engine)
cam.release()
cv2.destroyAllWindows()