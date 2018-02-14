
# functions: 5-20 lines of code
#

import tkinter
from tkinter import ttk
import time


import mqtt_remote_method_calls as com


def main():
    mqtt_client = com.MqttClient()
    mqtt_client.connect_to_ev3()

    # root = tkinter.Tk()
    # root.title("Robit!")
    #
    # main_frame = ttk.Frame(root, padding=20, relief='raised')
    # main_frame.grid()
    #
    # left_speed_label = ttk.Label(main_frame, text="Left")
    # left_speed_label.grid(row=0, column=0)
    # left_speed_entry = ttk.Entry(main_frame, width=8)
    # left_speed_entry.insert(0, "600")
    # left_speed_entry.grid(row=1, column=0)
    #
    # right_speed_label = ttk.Label(main_frame, text="Right")
    # right_speed_label.grid(row=0, column=2)
    # right_speed_entry = ttk.Entry(main_frame, width=8, justify=tkinter.RIGHT)
    # right_speed_entry.insert(0, "600")
    # right_speed_entry.grid(row=1, column=2)




