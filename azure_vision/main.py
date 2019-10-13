import cv2
import sys
import threading

from quick_train_tf_agent.python.predict import main as predmain

class Camera:
    def __init__(self):
        self.point1 = (0,0)
        self.point2 = (0,0)

    # should be a smooth video experience
    def display_vid(self, cam):
        img_counter = 0


        while True:
            img_counter += 1
            ret, frame = cam.read()
            # print(self.point1)
            cv2.rectangle(frame, self.point1, self.point2, 150, 10)
            cv2.imshow("test", frame)
            if(img_counter % 105 == 0):
                img_counter = 1
                t2 = threading.Thread(target=self.analysis, args=(ret,frame,))
                t2.start()

            k = cv2.waitKey(1)
            if k%256 == 27:
            # ESC pressed
                print("Escape hit, closing...")
                break

    # takes 3.5 seconds to complete each analysis
    def analysis(self, ret, frame):
        height, width = frame.shape[:2]
        cv2.imwrite("./frame%d.jpg" % ret, frame)

        prediction = predmain("./frame1.jpg")

        if prediction == 0:
            self.point1 = (0,0)
            self.point2 = (0,0)
            return 1

        left = prediction['boundingBox']
        left = left["left"]
        top = prediction['boundingBox']
        top = top['top']
        width_bb = prediction['boundingBox']
        width_bb = width_bb['width']
        height_bb = prediction['boundingBox']
        height_bb = height_bb['height']

        left = abs(int(width*left))
        top = abs(int(top*height))

        self.point1 = (left, top)
        self.point2 = (int(left+(width_bb*width)), int(top+(height_bb*height)))
        # print(self.point1, self.point2)
        print("Over 50")

    def start(self):
        cam = cv2.VideoCapture(0)
        cv2.namedWindow("test")
        self.display_vid(cam)
        cam.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    app = Camera()
    app.start()