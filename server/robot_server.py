#!/usr/bin/python3
import socket
import sys
import time

#import ncs
import camera
import telebotics
import bottom_half
import settings as st

#### init ####
camera.init()
#ncs.init('googlenet')
telebotics.init('', int(sys.argv[1]))
bottom_half.init()
##############

telebotics.accept_connection()

#old_time = time.time()

try:
    local_index = 0
    while True:
        if (local_index < telebotics.index):
            local_index = telebotics.index

            #time0 = time.time()

            try:
                telebotics.send_frame()
                telebotics.send_string('Placeholder 0')
                telebotics.send_string('Placeholder 1')
                telebotics.send_string('Placeholder 2')
                telebotics.send_string('Placeholder 3')
                telebotics.send_string('Placeholder 4')
                #telebotics.send_string(st.labels[st.order[0]])
                #telebotics.send_string(st.labels[st.order[1]])
                #telebotics.send_string(st.labels[st.order[2]])
                #telebotics.send_string(st.labels[st.order[3]])
                #telebotics.send_string(st.labels[st.order[4]])
                telebotics.send_string(str(bottom_half.getBump()))

                # receieve a key from client, and show it
                command = telebotics.recv_command()

                if (command == "C8"):
                    bottom_half.cam_up();
                elif (command == "C2"):
                    bottom_half.cam_down();
                elif (command == "C4"):
                    bottom_half.cam_left();
                elif (command == "C6"):
                    bottom_half.cam_right();
                elif (command == "C0"):
                    bottom_half.cam_position(0, 0, True)
                elif (command == "C5"):
                    bottom_half.cam_position(1000, 0, True)
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
                elif (command == "L1"):
                    bottom_half.light(True)
                elif (command == "L0"):
                    bottom_half.light(False)

            except socket.error as msg:
                telebotics.disconnected()
                print ('Connection closed')
                print ('Wait for new connection')
                telebotics.accept_connection()
                #old_time = time.time()

            #time1 = time.time()
            #print (str(local_index) + ": send data (" + str(len(data)) + " bytes) took "
            #        + str(1000*(time1 - time0)) + " ms")
        time.sleep(0.0001)

finally:
    print ("closing")
    bottom_half.close()
