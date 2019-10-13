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
    height, width = frame.shape[:2]
    print("success")
    cv2.imwrite("./frame%d.jpg" % ret, frame)
    prediction = predict.main("./frame1.jpg")

    left = prediction['boundingBox'['Left']]
    top = prediction['boundingBox']['Top']
    width_bb = prediction['boundingBox']['Width']
    height_bb = prediction['boundingBox']['Height']

    left = width*left
    top = top*height

    point1 = (left, top)
    point2 = (left+(width_bb*width), top+(height_bb*height))

    cv2.rectangle(frame, point1, point2, 255, 3)


display_vid(cam)
cam.release()
cv2.destroyAllWindows()