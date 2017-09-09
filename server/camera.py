#!/usr/bin/python3
import time
import settings as st

def grab_frame(threadName, cap):
    st.frame_index = 0
    while True:
        #begin = time.time()
        _, cap_frame = cap.read()
        st.frame = cap_frame[0:1079, 420:1499]
        st.frame_index = st.frame_index + 1
        #end = time.time()
        #print ("capture frame in " + str(end-begin) + " s")
