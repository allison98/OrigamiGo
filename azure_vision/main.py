import cv2
import sys
sys.path.append("front_init_agent/python/")
import predict
cam = cv2.VideoCapture(0)
print('success')

cv2.namedWindow("test")

img_counter = 0

while True:
    ret, frame = cam.read()
    cv2.imshow("test", frame)
    if not ret:
        break
    cv2.imwrite("./frame%d.jpg" % ret, frame)
    k = cv2.waitKey(1)
    if k%256 == 27:
        # ESC pressed
        print("Escape hit, closing...")
        break

cam.release()

cv2.destroyAllWindows()