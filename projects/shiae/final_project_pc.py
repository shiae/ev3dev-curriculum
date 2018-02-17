
# functions: 5-20 lines of code
#

import tkinter
from tkinter import ttk, StringVar
import mqtt_remote_method_calls as com


class MyDelegate(object):
    def scared_of_red(self):
        root = tkinter.Tk()
        root.title = "I don't like red"
        label = ttk.Label(root, text="I don't like red!")
        label.grid()
        frame = ttk.Frame(root, padding=30)
        frame.grid()
        root.mainloop()


my_delegate = MyDelegate()
mqtt_client = com.MqttClient(my_delegate)
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

