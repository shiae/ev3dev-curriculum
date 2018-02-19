
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

    label0 = ttk.Label(root, text=" ", font=('Helvetica', 10))
    label0.grid(row=0, column=0)

    label2 = ttk.Label(root, text=" ", font=('Helvetica', 10))
    label2.grid(row=1, column=0)

    label1 = ttk.Label(root, text="What do you want Robit to do?",
                       font=("Helvetica", 17))
    label1.grid(row=2, column=0)

    frame1 = ttk.Frame(root, padding=70)
    frame1.grid()

    command(frame1, root)


def command(frame, root):
    command_var = StringVar()
    command_box = ttk.Combobox(frame, textvariable=command_var,
                               font=("Helvetica", 12))
    command_box.bind('<<Combobox Selected>>', print('command_ev3'))
    command_box['values'] = ('Fetch', 'Sit', 'Shake', 'Come', 'Speak')
    command_box.grid(column=0, row=3)

    style = ttk.Style()
    style.configure('my.TButton', font=('Helvetica', 12))

    speak_btn = ttk.Button(frame, text="Bark Bark", style='my.TButton')
    speak_btn.grid(column=0, row=4)
    speak_btn.state(["disabled"])

    send_btn = ttk.Button(frame, text="Send", style='my.TButton')
    send_btn.grid(column=1, row=3)
    send_btn['command'] = lambda: check(command_var.get(), speak_btn)

    root.mainloop()


def check(command_input, speak_btn):
    if command_input == 'Speak':
        speak_btn.state(["!disabled"])
        # speak_btn[command] = lambda: mqtt_client.send_message('speak')
        print("speak")
    elif command_input == 'Fetch':
        # mqtt_client.send_message('fetch')
        speak_btn.state(["disabled"])
        print("fetch")
    elif command_input == 'Sit':
        # mqtt_client.send_message('sit')
        speak_btn.state(["disabled"])
        print("sit")
    elif command_input == 'Come':
        # mqtt_client.send_message('come')
        speak_btn.state(["disabled"])
        print("come")
    elif command_input == 'Shake':
        # mqtt_client.send_message('shake')
        speak_btn.state(["disabled"])
        print("shake")


main()
