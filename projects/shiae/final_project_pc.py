
# functions: 5-20 lines of code
#

import tkinter
from tkinter import ttk, StringVar
import mqtt_remote_method_calls as com


class MyDelegate(object):
    # def scared_of_red(self):
    #     root = tkinter.Tk()
    #     root.title = "I don't like red"
    #     label = ttk.Label(root, text="I don't like red!")
    #     label.grid()
    #     frame = ttk.Frame(root, padding=30)
    #     frame.grid()
    #     root.mainloop()

    def love(self):
        root = tkinter.Tk()
        # root.title = "Thanks for feeding me!"
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
    root.title = "Robit"
    label = ttk.Label(root, text="What do you want Robit to do?")
    label.grid(row=0, column=0)
    frame1 = ttk.Frame(root, padding=100)
    frame1.grid()
    command(frame1)

    root.mainloop()


def command(frame):
    command_var = StringVar()
    command_box = ttk.Combobox(frame, textvariable=command_var)
    command_box.bind('<<Combobox Selected>>', print('command_ev3'))
    command_box['values'] = ('Fetch', 'Sit', 'Shake', 'Come', 'Speak')
    command_box.grid(column=0, row=1)
    speak_btn = ttk.Button(frame, text="Bark Bark")
    speak_btn.grid(column=0, row=2)
    speak_btn.state(["disabled"])
    if command_box.get == 'Speak':
        speak_btn.state(["!disabled"])
        # speak_btn[command] = lambda: mqtt_client.send_message('speak')
        print("speak")
    elif command_box.get() == 'Fetch':
        # mqtt_client.send_message('fetch')
        print("fetch")
    elif command_box.get() == 'Sit':
        # mqtt_client.send_message('sit')
        print("sit")
    elif command_box.get() == 'Come':
        # mqtt_client.send_message('come')
        print("come")
    elif command_box.get() == 'Shake':
        # mqtt_client.send_message('shake')
        print("shake")
    # send_btn = ttk.Button(frame, text="send")
    # send_btn.grid(column=1, row=1)
    # send_btn[command] = lambda: send(command_box.get())

# def send(selected):
#     if selected == 'Speak':
#         speak_btn.state(["!disabled"])
#         # speak_btn[command] = lambda: mqtt_client.send_message('speak')
#         print("speak")
#     elif selected == 'Fetch':
#         # mqtt_client.send_message('fetch')
#         print("fetch")
#     elif command_box.get() == 'Sit':
#         # mqtt_client.send_message('sit')
#         print("sit")
#     elif command_box.get() == 'Come':
#         # mqtt_client.send_message('come')
#         print("come")
#     elif command_box.get() == 'Shake':
#         # mqtt_client.send_message('shake')
#         print("shake")


main()
