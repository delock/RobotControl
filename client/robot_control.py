#!/usr/bin/python3
import sys
import time
import io
import threading

from kivy.config import Config

window_width = 1920
window_height = 1080

Config.set('graphics', 'left', '0')
Config.set('graphics', 'top', '0')
Config.set('graphics', 'width', str(window_width))
Config.set('graphics', 'height', str(window_height))
Config.set('graphics', 'borderless', '1')


from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.core.image import Image as CoreImage
from kivy.core.window import Window
from kivy.graphics import *
from kivy.clock import Clock

import networks
import fps

class CameraFeed(Image):
    def __init__(self, **kwargs):
        super(Image, self).__init__(**kwargs)
        self.allow_stretch = True

    def update_bg(self, im):
        tex = im.texture
        with self.canvas:
            self.texture = tex

class RobotControl(App):
    def action_thread(self):
        global stop_flag

        networks.init(sys.argv[1], int(sys.argv[2]))

        old_time = time.time()

        self.command = "00"
        while True:
            compressed_frame = networks.recvFrame()
            data = io.BytesIO(compressed_frame)
            self.im = CoreImage(data, ext="jpg")

            self.label_1.text = networks.recvString()
            self.label_2.text = networks.recvString()
            self.label_3.text = networks.recvString()
            self.label_4.text = networks.recvString()
            self.label_5.text = networks.recvString()

            networks.sendString(self.command)

            cur_time = time.time()
            cur_fps = fps.getFPS(cur_time - old_time)
            self.label_fps.text = "FPS: " + str(cur_fps)
            old_time = cur_time
            if (stop_flag):
                break

    def on_refresh(self, dt):
        if (self.im != None):
            self.camera_feed.update_bg(self.im)
        return True

    def on_start(self):
        threading.Thread(target=self.action_thread).start()
        event = Clock.schedule_interval(self.on_refresh, 1/30.)
        self.keyboard = Window.request_keyboard(self.keyboard_closed, self)
        self.keyboard.bind(on_key_down=self.on_keyboard_down)
        self.keyboard.bind(on_key_up=self.on_keyboard_up)

    def keyboard_closed(self):
        self.keyboard.unbind(on_key_down=self.on_keyboard_down)
        self.keyboard.unbind(on_key_up=self.on_keyboard_up)

    def on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if keycode[1] == 'w':
            self.command = "W8"
        elif keycode[1] == 's':
            self.command = "W2"
        elif keycode[1] == 'a':
            self.command = "W4"
        elif keycode[1] == 'd':
            self.command = "W6"
        elif keycode[1] == 'q':
            self.command = "W7"
        elif keycode[1] == 'e':
            self.command = "W9"

        elif keycode[1] == '1':
            self.command = "L1"
        elif keycode[1] == '2':
            self.command = "L0"

        elif keycode[1] == 'up':
            self.command = "C8"
        elif keycode[1] == 'down':
            self.command = "C2"
        elif keycode[1] == 'left':
            self.command = "C4"
        elif keycode[1] == 'right':
            self.command = "C6"
        elif keycode[1] == 'pageup':
            self.command = "C0"
        elif keycode[1] == 'pagedown':
            self.command = "C5"

        if keycode[1] == 'escape':
            keyboard.release()
            return False
        else:
            return True

    def on_keyboard_up(self, keyboard, keycode):
        self.command = "00"
        return True

    def build(self):
        middle_portion = window_height/window_width
        side_portion = (1-middle_portion)/2
        label_layout = GridLayout(cols=1, size_hint=(side_portion, 0.5), pos_hint={'x':1-side_portion, 'y':0.5})

        self.label_1 = Label(text="rank-1")
        self.label_2 = Label(text="rank-2")
        self.label_3 = Label(text="rank-3")
        self.label_4 = Label(text="rank-4")
        self.label_5 = Label(text="rank-5")
        self.label_fps = Label(text="fps")

        self.im = None
        self.camera_feed = CameraFeed(size_hint=(middle_portion, 1.0), pos_hint={'x':side_portion, 'y':0})

        label_layout.add_widget(self.label_1)
        label_layout.add_widget(self.label_2)
        label_layout.add_widget(self.label_3)
        label_layout.add_widget(self.label_4)
        label_layout.add_widget(self.label_5)
        label_layout.add_widget(self.label_fps)

        top_layout = FloatLayout(size=(1920,1080))
        top_layout.add_widget(self.camera_feed)
        top_layout.add_widget(label_layout)

        return top_layout

global stop_flag

stop_flag = False
RobotControl().run()
stop_flag = True

