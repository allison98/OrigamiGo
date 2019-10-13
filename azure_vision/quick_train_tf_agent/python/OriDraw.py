import cv2
import os
import sys
import numpy as np
import tkinter
import pyttsx3
from threading import Thread

from predict import main as predmain


i = 0
class OriDraw:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.frame = None
        self.exit = 0
        self.corners = None
        self.new = 0
        self.step = 0
        self.detected = 0
        self.speech = 0 
        self.point1 = (0,0)
        self.point2 = (0,0)
        self.point3 = (0,0)
        self.point4 = (0,0)
        self.img_counter = 0
        self.message = ''
       
    def draw_square(self):
        self.frame = cv2.line(self.frame,(self.x1,self.y1),(self.x2,self.y2),(0,0,0),5)
        self.frame = cv2.line(self.frame,(self.x2,self.y2),(self.x3,self.y3),(0,0,0),5)
        self.frame = cv2.line(self.frame,(self.x3,self.y3),(self.x4,self.y4),(0,0,0),5)
        self.frame = cv2.line(self.frame,(self.x4,self.y4),(self.x1,self.y1),(0,0,0),5)


    def delete_bg(self):
        pass

    def update(self):
        self.img_counter +=1
        ret, self.frame = self.cap.read()
        self.frame = cv2.flip(self.frame,1)
        cv2.rectangle(self.frame, self.point1, self.point2, 150, 10)
        
        if(self.img_counter % 105 == 0):
                self.img_counter = 1
                t2 = Thread(target=self.analysis, args=(ret,self.frame,))
                t2.start()

        if self.step == 1:
            self.get_corners()
            #self.draw_square()
            # fp = self.corners[0]
            # sp = self.corners[2]
            # self.frame = cv2.line(self.frame,fp,sp,255,5)
            self.draw_diag_crease()
            self.speech = 1
            self.step = 0
            # TO DO 
        if self.step == 2:
            self.get_corners()
            self.speech = 1
            self.step = 0
        if self.step == 3:
            self.get_corners()
            self.speech = 1
            self.step = 0
        if self.step == 4:
            self.get_corners()
            self.speech = 1
            self.step = 0         
        if self.step == 5:
            self.get_corners()
            self.speech = 1
            self.step = 0
        if self.step == 6:
            self.get_corners()
            self.speech = 1
            self.step = 0  
                

        cv2.imshow('OrigamiGO', self.frame)

        if self.speech == 1:
            t2 = Thread(target=self.speak, args=(self.message,))
            t2.start()
          #  self.speak('This is Step 1')
            self.speech = 0
            

        key = cv2.waitKey(1)
        if key == 13: #13 is the Enter Key
            self.exit = 1
            return
        elif key == ord('r'):
            self.step = 0

    def speak(self, key):
        engine = pyttsx3.init()
        # engine.setProperty('rate', 300)   
        voices = engine.getProperty('voices')       #getting details of current voice
        engine.setProperty('voice', voices[0].id)  #changing index, changes voices. o for male
        # engine.setProperty('voice', voices[1].id)   #  # setting up new voice rate
        engine.say(key)
        engine.runAndWait()

    #must figure out what the step is
    def get_step(self):
        pass

    def get_corners(self):
        #corners = Corners()
        if self.new == 0:
            self.i = 0
            self.new = 1

        height, width = self.frame.shape[:2]
        print(height, width)
        if self.i > 30 or self.i is None:
            self.i = 0
        if self.i < 200:
            self.i+=1
            self.x1,self.y1 = 0+self.i,0+self.i
            self.x2,self.y2 = 250+self.i, 0+self.i
            self.x3,self.y3 = 250+self.i, 250+self.i
            self.x4,self.y4 = 0+self.i, 250+self.i
        
        self.corners = [(self.x1,self.y1), (self.x2,self.y2), (self.x3,self.y3), (self.x4,self.y4)]
    
    def draw_diag_crease(self):
        self.frame = cv2.line(self.frame,self.point1,self.point2,(0,0,0),5)
        self.frame = cv2.line(self.frame,self.point3,self.point4,(0,0,0),5)

        
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

        step_name = prediction["tagName"]
        if step_name == 'front_init' or step_name =='back_init':
            self.step = 1
            self.message = 'Let us begin. Crease diagonally in both directions. Fold one corner into the intersection of the creases or the middle.'
        elif step_name == 'second':
            self.step = 2
            self.message = 'Good job! Now fold the opposite flap to the edge of the first flap.'
        elif step_name == 'third':
            self.step =3
            self.message = 'Fold the left flap into the middle like shown on the screen'
        elif step_name == 'fourth_left':
            self.step = 4
            self.message = 'Fold the right flap into the middle like shown on the screen'
        elif step_name =='fifth':
            self.step = 5
            self.message = 'Fold the top edges back to round the corners.'
        elif step_name =="finished":
            self.step = 6
            self.message = 'Good job, You have compeleted an origami heart.'
        else:
            self.step = 0
        print("step: "+str(self.step))

        self.point1 = (left, top)
        self.point2 = (int(left+(width_bb*width)), int(top+(height_bb*height)))
        self.point3 = (left, int(top+(height_bb*height)))
        self.point4 = (int(left+(width_bb*width)), top)
        # print(self.point1, self.point2)

        print("Matched")

if __name__ == "__main__":
    app = OriDraw()
    while True:
        app.update()
        if app.exit:
            break
