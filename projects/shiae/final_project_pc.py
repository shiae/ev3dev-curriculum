"""
My final project turns the ev3 robot into a dog, who I call Robit. Robit can
speak, come, sit, fetch, and shake.

This file is meant to be run on a pc. When run, a window will pop up with a
drop down box and two buttons. The user selects an option from the drop down
box, and clicks send. This command will be sent to Robit. If "Speak" is
selected, the "Bark Bark" button will be enabled. Each time the "Bark Bark"
button is pressed, Robit will say "bark bark."

Author: Allison Shi, February 2018
"""

import tkinter
from tkinter import ttk, StringVar
import mqtt_remote_method_calls as com


class MyDelegate(object):
    """ Creates an object used as a delegate for MQTT(for receiving messages
    from ev3)"""
    # def scared_of_red(self):
    #     root = tkinter.Tk()
    #     root.title = "I don't like red"
    #     label = ttk.Label(root, text="I don't like red!")
    #     label.grid()
    #     frame = ttk.Frame(root, padding=30)
    #     frame.grid()
    #     root.mainloop()

    def love(self):
        """ When Robit's color sensor senses red, a window with a hear gif pops up"""
        root = tkinter.Tk()
        hearts = tkinter.PhotoImage(file="hearts.gif")
        label = ttk.Label(root, image=hearts)
        label.grid()
        frame = ttk.Frame(root, padding=30)
        frame.grid()
        root.mainloop()


my_delegate = MyDelegate()
mqtt_client = com.MqttClient(my_delegate)
mqtt_client.connect_to_ev3()


def main():
    root = tkinter.Tk()
    root.title("Robit")
    style = ttk.Style()

    label0 = ttk.Label(root, text=" ", font=('Helvetica', 10))
    label0.grid(row=0, column=0)

    label1 = ttk.Label(root, text="What do you want Robit to do?",
                       font=("Helvetica", 17))
    label1.grid(row=2, column=0)

    style.configure('my.TFrame', background='#a8c9ff')
    frame1 = ttk.Frame(root, style='my.TFrame', padding=70)
    frame1.grid()

    command(frame1, root)


def command(frame, root):
    """ Creates a drop down for the different commands Robit can receive."""
    style = ttk.Style()
    style.configure('my.TButton', font=('Helvetica', 12), background='#002663',
                    padding=5)

    command_var = StringVar()
    command_box = ttk.Combobox(frame, textvariable=command_var,
                               font=("Helvetica", 12))
    command_box.bind('<<Combobox Selected>>', print('command_ev3'))
    command_box['values'] = ('Fetch', 'Sit', 'Shake', 'Come', 'Speak')
    command_box.grid(column=0, row=3)

    speak_btn = ttk.Button(frame, text="Bark Bark", style='my.TButton')
    speak_btn.grid(column=0, row=5)
    speak_btn.state(["disabled"])

    # label4 = ttk.Label(root, text="hello", font=('Helvetica', 10))
    # label4.grid(row=0, column=1)

    send_btn = ttk.Button(frame, text="Send", style='my.TButton')
    send_btn.grid(column=2, row=3)
    send_btn['command'] = lambda: check(command_var.get(), speak_btn)

    root.mainloop()


def check(command_input, speak_btn):
    """ Decides what message to send to Robit based on command selected."""
    if command_input == 'Speak':
        speak_btn.state(["!disabled"])
        speak_btn['command'] = lambda: mqtt_client.send_message('speak')
        print("speak")
    elif command_input == 'Fetch':
        mqtt_client.send_message('fetch')
        speak_btn.state(["disabled"])
        print("fetch")
    elif command_input == 'Sit':
        mqtt_client.send_message('sit')
        speak_btn.state(["disabled"])
        print("sit")
    elif command_input == 'Come':
        mqtt_client.send_message('come')
        speak_btn.state(["disabled"])
        print("come")
    elif command_input == 'Shake':
        mqtt_client.send_message('shake')
        speak_btn.state(["disabled"])
        print("shake")


main()
