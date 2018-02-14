
# functions: 5-20 lines of code
#

import ev3dev.ev3 as ev3
import time

import tkinter
from tkinter import ttk

import mqtt_remote_method_calls as com
import robot_controller as robo

robit = robo.Snatch3r()

robit.loop_forever()  # Calls a function that has a while True: loop within
# it to avoid letting the program end.


