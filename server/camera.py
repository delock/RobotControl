#!/usr/bin/python3
import cv2
import _thread as thread
import time
import settings as st
import bottom_half

global cap_width
global cap_height
global frame_rate

#cap_width = 3264
#cap_height = 2448

#cap_width = 2592
#cap_height = 1944

cap_width = 2048
cap_height = 1536

#cap_width = 1600
#cap_height = 1200

frame_rate = 20
#cap_width = 1920
#cap_height = 1080

def init():
    global cap
    global cap_width
    global cap_height
    global frame_rate

    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FPS, frame_rate)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, cap_width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, cap_height)
    cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))

    _, st.frame = cap.read()
    st.frame_index = 0

    thread.start_new_thread (grab_frame, ("Capture thread", cap))

def grab_frame(threadName, cap):
    global cap_width
    global cap_height
    global cam_pitch
    st.frame_index = 0
    try:
        while True:
            if (st.verbose):
                begin = time.time()

            _, cap_frame = cap.read()
            blank_width = int((cap_width-cap_height)/2)
            blank_offset = int(0.03*cap_width)
            temp_frame = cap_frame[0:cap_height-1, blank_width+blank_offset:cap_width-blank_width-1+blank_offset]
            if bottom_half.cam_pitch < 0:
                temp_frame = cv2.flip(temp_frame, -1)
            #frame_trim = int(cap_height*(1-1/1.5)/2)
            #center_frame = temp_frame[frame_trim:cap_height-1-frame_trim, frame_trim:cap_height-1-frame_trim]
            #st.frame = center_frame
            st.frame = temp_frame
            st.frame_index = st.frame_index + 1

            if (st.verbose):
                end = time.time()
                print ("capture frame in " + str(1/(end-begin)) + " fps")
    finally:
        close()

def close():
    global cap
    cap.release()
