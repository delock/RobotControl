#!/usr/bin/python3
import socket
import sys
import time

import ncs
import camera
import telemetry
import bottom_half
import settings as st

#### init ####
camera.init()
ncs.init('googlenet')
telemetry.init('', int(sys.argv[1]))
bottom_half.init()
##############

telemetry.accept_connection()

#old_time = time.time()

try:
    local_index = 0
    while True:
        if (local_index < telemetry.index):
            local_index = telemetry.index

            #time0 = time.time()

            try:
                telemetry.send_frame()
                telemetry.send_string(st.labels[st.order[0]])
                telemetry.send_string(st.labels[st.order[1]])
                telemetry.send_string(st.labels[st.order[2]])
                telemetry.send_string(st.labels[st.order[3]])
                telemetry.send_string(st.labels[st.order[4]])

                # receieve a key from client, and show it
                command = telemetry.recv_command()

                if (command == "C8"):
                    bottom_half.cam_up();
                elif (command == "C2"):
                    bottom_half.cam_down();
                elif (command == "C4"):
                    bottom_half.cam_left();
                elif (command == "C6"):
                    bottom_half.cam_right();
                elif (command == "C0"):
                    bottom_half.cam_position(0, 0)
                elif (command == "C5"):
                    bottom_half.cam_position(1000, 0)
                elif (command == "W8"):
                    bottom_half.wheel_forward()
                elif (command == "W5"):
                    bottom_half.wheel_stop()
                elif (command == "W2"):
                    bottom_half.wheel_backward()
                elif (command == "W4"):
                    bottom_half.wheel_left()
                elif (command == "W6"):
                    bottom_half.wheel_right()
                elif (command == "W7"):
                    bottom_half.wheel_speed(200, 1000)
                elif (command == "W9"):
                    bottom_half.wheel_speed(1000, 200)
                elif (command == "W1"):
                    bottom_half.wheel_speed(-200, -1000)
                elif (command == "W3"):
                    bottom_half.wheel_speed(-1000, -200)

                #print (command)
            except socket.error as msg:
                telemetry.disconnected()
                print ('Connection closed')
                print ('Wait for new connection')
                telemetry.accept_connection()
                print ('Connected from ' + str(addr))
                #old_time = time.time()

            #time1 = time.time()
            #print (str(local_index) + ": send data (" + str(len(data)) + " bytes) took "
            #        + str(1000*(time1 - time0)) + " ms")
        time.sleep(0.0001)

finally:
    print ("closing")
    telemetry.close()
    ncs.close()
    bottom_half.close()
    camera.close()
