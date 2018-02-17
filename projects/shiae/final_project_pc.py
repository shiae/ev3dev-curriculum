
# functions: 5-20 lines of code
#

import tkinter
from tkinter import ttk, StringVar
import mqtt_remote_method_calls as com
mqtt_client = com.MqttClient()
mqtt_client.connect_to_ev3()


def main():
    root = tkinter.Tk()
    root.title = "Robit"
    label = ttk.Label(root, text="What do you want Robit to do?")
    label.grid(row=0, column=0)
    frame1 = ttk.Frame(root, padding=30)
    frame1.grid()
    # speak_button(frame1)
    command(frame1)


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
    command_box.grid(column=0, row=1)
    if command_box.get() == "Speak":
        mqtt_client.send_message('speak_ev3')
    elif command_box.get() == "Fetch":
        mqtt_client.send_message('fetch')
    elif command_box.get() == "Sit":
        mqtt_client.send_message('sit')


main()

