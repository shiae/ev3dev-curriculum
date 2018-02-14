"""


"""

import ev3dev.ev3 as ev3
import time

import tkinter
from tkinter import ttk

import mqtt_remote_method_calls as com
import robot_controller as robo


def main():
    robit = robo.Snatch3r()
    mqtt_client = com.MqttClient(robit)
    mqtt_client.connect_to_pc()
    robit.loop_forever()  # Calls a function that has a while True: loop within
    # it to avoid letting the program end.