#!/usr/bin/python3
import sys
import time
import io
import threading

from kivy.config import Config

#window_width = 3840
#window_height = 2160
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
from kivy.uix.button import Button
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

    light = 0
    def button_callback(self, instance, value):
        if (instance == self.button_w and value == "down"):
            self.command = "W8"
        elif (instance == self.button_a and value == "down"):
            self.command = "W4"
        elif (instance == self.button_s and value == "down"):
            self.command = "W2"
        elif (instance == self.button_d and value == "down"):
            self.command = "W6"

        elif (instance == self.button_left and value == "down"):
            self.command = "C4"
        elif (instance == self.button_right and value == "down"):
            self.command = "C6"
        elif (instance == self.button_up and value == "down"):
            self.command = "C8"
        elif (instance == self.button_down and value == "down"):
            self.command = "C2"

        elif (instance == self.button_top and value == "down"):
            self.command = "C0"
        elif (instance == self.button_front and value == "down"):
            self.command = "C5"

        elif (instance == self.button_light and value == "down"):
            self.light = 1-self.light
            if (self.light == 1):
                self.command = "L1"
                instance.text = "#"
            if (self.light == 0):
                self.command = "L0"
                instance.text = "-"

        else:
            self.command = "00"

    def build(self):
        middle_portion = window_height/window_width
        side_portion = (1-middle_portion)/2
        side_pix = (window_width - window_height)/2
        label_layout = GridLayout(cols=1, size_hint=(side_portion, 0.3), pos_hint={'x':1-side_portion, 'y':0.7})

        self.label_1 = Label(text="rank-1", font_size='40sp', text_size = (side_pix, 40))
        self.label_2 = Label(text="rank-2", font_size='35sp', text_size = (side_pix, 35))
        self.label_3 = Label(text="rank-3", font_size='30sp', text_size = (side_pix, 30))
        self.label_4 = Label(text="rank-4", font_size='25sp', text_size = (side_pix, 25))
        self.label_5 = Label(text="rank-5", font_size='20sp', text_size = (side_pix, 20))
        self.label_fps = Label(text="fps", font_size='40sp', text_size = (side_pix, 40))

        self.button_w = Button(text="W", font_size = '40sp', size_hint = (side_portion/4, 0.1),
                                                             pos_hint = {'x': (side_portion/3), 'y':0.24})
        self.button_a = Button(text="A", font_size = '40sp', size_hint = (side_portion/4, 0.1),
                                                             pos_hint = {'x': 0, 'y':0.12})
        self.button_s = Button(text="S", font_size = '40sp', size_hint = (side_portion/4, 0.1),
                                                             pos_hint = {'x': (side_portion/3), 'y':0})
        self.button_d = Button(text="D", font_size = '40sp', size_hint = (side_portion/4, 0.1),

                                                             pos_hint = {'x': (side_portion*2/3), 'y':0.12})
        self.button_up = Button(text="^", font_size = '40sp', size_hint = (side_portion/4, 0.1),
                                                             pos_hint = {'x': (1-side_portion)+(side_portion/3), 'y':0.24})
        self.button_left = Button(text="<", font_size = '40sp', size_hint = (side_portion/4, 0.1),
                                                             pos_hint = {'x': (1-side_portion), 'y':0.12})
        self.button_down = Button(text="v", font_size = '40sp', size_hint = (side_portion/4, 0.1),
                                                             pos_hint = {'x': (1-side_portion)+(side_portion/3), 'y':0})
        self.button_right = Button(text=">", font_size = '40sp', size_hint = (side_portion/4, 0.1),
                                                             pos_hint = {'x': (1-side_portion)+(side_portion*2/3), 'y':0.12})

        self.button_top = Button(text="skyview", font_size = '20sp', size_hint = (side_portion/4, 0.1),
                                                             pos_hint = {'x': (1-side_portion)+(side_portion/3), 'y':0.52})
        self.button_front = Button(text="frontview", font_size = '20sp', size_hint = (side_portion/4, 0.1),
                                                             pos_hint = {'x': (1-side_portion)+(side_portion/3), 'y':0.4})

        self.button_light = Button(text="-", font_size = '40sp', size_hint = (side_portion/4, 0.1),
                                                             pos_hint = {'x': (side_portion/3), 'y':0.4})

        self.button_w.bind(state=self.button_callback)
        self.button_a.bind(state=self.button_callback)
        self.button_s.bind(state=self.button_callback)
        self.button_d.bind(state=self.button_callback)
        self.button_up.bind(state=self.button_callback)
        self.button_down.bind(state=self.button_callback)
        self.button_left.bind(state=self.button_callback)
        self.button_right.bind(state=self.button_callback)
        self.button_top.bind(state=self.button_callback)
        self.button_front.bind(state=self.button_callback)
        self.button_light.bind(state=self.button_callback)

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

        top_layout.add_widget(self.button_w)
        top_layout.add_widget(self.button_a)
        top_layout.add_widget(self.button_s)
        top_layout.add_widget(self.button_d)

        top_layout.add_widget(self.button_up)
        top_layout.add_widget(self.button_down)
        top_layout.add_widget(self.button_left)
        top_layout.add_widget(self.button_right)

        top_layout.add_widget(self.button_light)

        top_layout.add_widget(self.button_top)
        top_layout.add_widget(self.button_front)

        return top_layout

global stop_flag

stop_flag = False
RobotControl().run()
stop_flag = True

