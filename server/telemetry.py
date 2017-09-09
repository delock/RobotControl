#!/usr/bin/python3
import cv2
import numpy as np
import socket
import sys
import pickle
import struct
import time
import settings as st

def compress_frame(threadName, cap):
    local_index = 0

    st.compressed_index = 0
    while True:
        if (st.connected and local_index < st.frame_index):
            #begin = time.time()
            local_frame = st.frame

            local_index = st.frame_index
            resize_frame = cv2.resize(local_frame, (500, 500))
            _,st.compressed_frame = cv2.imencode(".jpg", resize_frame, [int(cv2.IMWRITE_JPEG_QUALITY), 30])
            st.compressed_index = st.compressed_index + 1
            #end = time.time()
            #print ("compress frame in " + str(1000*(end-begin)) + " ms")
        time.sleep(0.0001)
