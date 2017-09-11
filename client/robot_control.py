#!/usr/bin/python3
import sys
import time
import io
import threading

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.core.image import Image as CoreImage
from kivy.graphics import *
from kivy.clock import Clock

import networks
import fps

class CameraFeed(Image):
    def update_bg(self, im):
        tex = im.texture
        with self.canvas:
            self.bg = Rectangle(texture=tex, pos=self.pos, size=self.size)

class RobotControl(App):
    def action_thread(self):
        networks.init(sys.argv[1], int(sys.argv[2]))

        old_time = time.time()

        command = "00"
        while True:
            compressed_frame = networks.recvFrame()
            data = io.BytesIO(compressed_frame)
            self.im = CoreImage(data, ext="jpg")

            self.label_1.text = networks.recvString()
            self.label_2.text = networks.recvString()
            self.label_3.text = networks.recvString()
            self.label_4.text = networks.recvString()
            self.label_5.text = networks.recvString()

            networks.sendString(command)

            cur_time = time.time()
            cur_fps = fps.getFPS(cur_time - old_time)
            self.label_fps.text = "FPS: " + str(cur_fps)
            old_time = cur_time

            #cv2.imshow('frame', resize_frame)
            #k = cv2.waitKey(1)
            #if k == 27:
            #    break
            #elif k==-1:
            #    command = "00"
            #elif k==113:  #Q
            #    command = "W7"
            #elif k==119:  #W
            #    command = "W8"
            #elif k==101:  #E
            #    command = "W9"
            #elif k==97:   #A
            #    command = "W4"
            #elif k==115:  #S
            #    command = "W2"
            #elif k==100:  #D
            #    command = "W6"
            #elif k==81:   #Left key
            #    command = "C4"
            #elif k==82:   #Up key
            #    command = "C8"
            #elif k==83:   #Right key
            #    command = "C6"
            #elif k==84:   #Down key
            #    command = "C2"
            #elif k==85:   #PgUp key
            #    command = "C0"
            #elif k==86:   #PgDn key
            #    command = "C5"
            #elif k==49:   #1 key
            #    command = "L1"
            #elif k==50:   #0 key
            #    command = "L0"
            #else:
            #    print("key=" + str(k))
            #    command = "01"

    def on_refresh(self, dt):
        print ("hello " + str(dt))
        self.camera_feed.update_bg(self.im)
        pass

    def on_start(self):
        threading.Thread(target=self.action_thread).start()
        event = Clock.schedule_interval(self.on_refresh, 1/30.)

    def build(self):
        label_layout = GridLayout(cols=1)

        self.label_1 = Label(text="rank-1")
        self.label_2 = Label(text="rank-2")
        self.label_3 = Label(text="rank-3")
        self.label_4 = Label(text="rank-4")
        self.label_5 = Label(text="rank-5")
        self.label_fps = Label(text="fps")

        self.camera_feed = CameraFeed()

        label_layout.add_widget(self.label_1)
        label_layout.add_widget(self.label_2)
        label_layout.add_widget(self.label_3)
        label_layout.add_widget(self.label_4)
        label_layout.add_widget(self.label_5)
        label_layout.add_widget(self.label_fps)

        top_layout = GridLayout(cols=2)
        top_layout.add_widget(self.camera_feed)
        top_layout.add_widget(label_layout)

        return top_layout

RobotControl().run()

