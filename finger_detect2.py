import cv2
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter
import math
import time

def main():
    global hand_hist
    is_hand_hist_created = False
    capture = cv2.VideoCapture(0)

    while capture.isOpened():
        pressed_key = cv2.waitKey(1)
        _, frame = capture.read()

        if pressed_key == 32:
            capture.release()
            cv2.destroyAllWindows()
            cv2.imwrite("capture2.jpeg", frame)
            
            
            generate_histogram()
            

        # if is_hand_hist_created:
        #     manage_image_opr(frame, hand_hist)

        # else:
        #     frame = draw_rect(frame)

        cv2.imshow("Live Feed", (frame))

        if pressed_key == 27:
            break

    cv2.destroyAllWindows()
    capture.release()

def generate_histogram():
    start = time.time()
    img = cv2.imread("capture2.jpeg")
    grayscale = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    b_l, b_r, blue_channel = channel_histogram(img, 0)
    g_l, g_r, green_channel = channel_histogram(img, 1)
    r_l, r_r, red_channel = channel_histogram(img, 2)

    l, r, gray_channel = channel_histogram(grayscale, -1)

    left_min = np.max([b_l, g_l, r_l])
    right_min = np.min([b_r, g_r, r_r])

    

    retval, gray_thresh = cv2.threshold(red_channel[:, :, 2], r_l, r_r, cv2.THRESH_BINARY)
    print(retval)
    cv2.imshow("red", gray_thresh)
    cv2.waitKey(0)
    

    plt.show()
    im2 = img.copy()
    im2 = blue_channel
    im2 += green_channel
    im2 += red_channel



    cv2.imshow("Image", im2)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    im2[im2 < left_min] = 0
    im2[im2 > right_min] = 0
    cv2.imshow("Image", im2)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    

def channel_histogram(img, channel):
    if (channel == -1):
        hist = np.ravel(cv2.calcHist(img, [0], None, [256], [0, 256]))
    else: 
        hist = np.ravel(cv2.calcHist(img, [channel], None, [256], [0, 256]))

    hist_filt = savgol_filter(hist, 7,5)

    max_val = np.max(hist_filt)
    
    max_val_loc = np.argwhere(hist_filt == max_val)
    cutoff = max_val/(math.exp(1))
    cutoff_diff_matrix = cutoff - hist_filt
    left_min = 0
    right_min = len(cutoff_diff_matrix) - 1

    for i in range(0, len(cutoff_diff_matrix)):
        if cutoff_diff_matrix[i] < 0:
            left_min = i
            break

    for i in range(1, len(cutoff_diff_matrix)+1):
        if(cutoff_diff_matrix[-1*i] < 0):
            right_min = len(cutoff_diff_matrix) - i 
            break
    plt.plot(hist_filt)
    plt.hlines(cutoff, 0, 255)

    imchan = img.copy()
    if (channel == 0):
        imchan[:, :, 1] = 0
        imchan[:, :, 2] = 0
    elif (channel == 1):
        imchan[:, :, 0] = 0
        imchan[:, :, 2] = 0
    elif (channel == 2):
        imchan[:, :, 0] = 0
        imchan[:, :, 1] = 0

        
    imchan[imchan < left_min] = 0
    imchan[imchan > right_min] = 0

    return left_min, right_min, imchan

    


main()


