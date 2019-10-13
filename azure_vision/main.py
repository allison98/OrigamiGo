import cv2
import sys
import threading
sys.path.append("front_init_agent/python/")
import predict
cam = cv2.VideoCapture(0)
cv2.namedWindow("test")


# should be a smooth video experience
def display_vid(cam):
    img_counter = 0

    while True:
        img_counter += 1
        ret, frame = cam.read()
        cv2.imshow("test", frame)
        if(img_counter % 105 == 0):
            img_counter = 1
            t2 = threading.Thread(target=analysis, args=(ret,frame,))
            t2.start()
        k = cv2.waitKey(1)
        if k%256 == 27:
        # ESC pressed
            print("Escape hit, closing...")
            break
# takes 3.5 seconds to complete each analysis
def analysis(ret,frame):
    print("success")
    cv2.imwrite("./frame%d.jpg" % ret, frame)
    predict.main("./frame1.jpg")


display_vid(cam)
cam.release()
cv2.destroyAllWindows()