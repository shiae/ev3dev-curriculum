
# functions: 5-20 lines of code
#

import tkinter
from tkinter import ttk, StringVar
import mqtt_remote_method_calls as com
mqtt_client = com.MqttClient()
mqtt_client.connect_to_ev3()


def main():
    root = tkinter.Tk()
    frame1 = ttk.Frame(root, padding=30)
    frame1.grid()
    # speak_button(frame1)
    command(frame1)
    # if something.get == "Speak"
    #   #     mqtt_client.send_message("speak_ev3")


    root.mainloop()


# def speak_button(frame):
#     hello_button = ttk.Button(frame, text="Speak")
#     hello_button['command'] = (lambda: speak_pc())
#     hello_button.grid()
#
#
# def speak_pc():
#     print("--------------------------------------------")
#     print(" Speak PC")
#     print("--------------------------------------------")
#     mqtt_client.send_message("speak_ev3")


def command(frame):
    command_var = StringVar()
    command_box = ttk.Combobox(frame, textvariable=command_var)
    command_box.bind('<<Combobox Selected>>', print('command_ev3'))
    command_box['values'] = ('Fetch', 'Sit', 'Shake')
    command_box.grid(column=0, row=0)


main()

