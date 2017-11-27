#!/usr/bin/python3
import cv2
import _thread as thread
import time
import settings as st

global cap_width
global cap_height
cap_width = 1920
cap_height = 1080

def init():
    global cap
    global cap_width
    global cap_height

    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, cap_width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, cap_height)
    cap.set(cv2.CAP_PROP_FPS, 30)

    _, st.frame = cap.read()
    st.frame_index = 0

    thread.start_new_thread (grab_frame, ("Capture thread", cap))

def grab_frame(threadName, cap):
    global cap_width
    global cap_height
    st.frame_index = 0
    try:
        while True:
            #begin = time.time()
            _, cap_frame = cap.read()
            blank_width = int((cap_width-cap_height)/2)
            temp_frame = cap_frame[0:cap_height-1, blank_width:cap_width-blank_width-1]
            frame_trim = int(cap_height*(1-1/1.5)/2)
            center_frame = temp_frame[frame_trim:cap_height-1-frame_trim, frame_trim:cap_height-1-frame_trim]
            st.frame = center_frame
            st.frame_index = st.frame_index + 1
            #end = time.time()
            #print ("capture frame in " + str(end-begin) + " s")
    finally:
        close()

def close():
    global cap
    cap.release()
