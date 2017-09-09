#!/usr/bin/python3
import cv2
import _thread as thread
import time
import settings as st

def init():
    global cap

    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
    cap.set(cv2.CAP_PROP_FPS, 30)

    _, st.frame = cap.read()
    st.frame_index = 0

    thread.start_new_thread (grab_frame, ("Capture thread", cap))

def grab_frame(threadName, cap):
    st.frame_index = 0
    while True:
        #begin = time.time()
        _, cap_frame = cap.read()
        st.frame = cap_frame[0:1079, 420:1499]
        st.frame_index = st.frame_index + 1
        #end = time.time()
        #print ("capture frame in " + str(end-begin) + " s")

def close():
    global cap
    cap.release()
