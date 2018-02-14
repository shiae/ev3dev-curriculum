
# functions: 5-20 lines of code
#

import tkinter
from tkinter import ttk
# import time
import mqtt_remote_method_calls as com


class MyDelegate(object):
    #   Creates an object which can write a message to a shared chat board.
    def __init__(self, label):
        self.label = label

    # def on_chat_message(self, message):
    #     self.label["text"] += "\n" + message


def main():
    root = tkinter.Tk()
    root.title = "Robit"

    main_frame = ttk.Frame(root, padding=20, relief='raised')
    main_frame.grid()

    label = ttk.Label(main_frame, justify=tkinter.LEFT,
                      text="My name is: ")
    label.grid(columnspan=2)

    msg_entry = ttk.Entry(main_frame, width=60)
    msg_entry.grid(row=2, column=0)

    msg_button = ttk.Button(main_frame, text="Send")
    msg_button.grid(row=2, column=1)
    msg_button['command'] = lambda: send_message(mqtt_client, robit,
                                                 chat_window, msg_entry)
    root.bind('<Return>',
              lambda event: send_message(mqtt_client, robit, chat_window,
                                         msg_entry))

    chat_window = ttk.Label(main_frame, justify=tkinter.LEFT, text="",
                            width=60, wraplength="500p")
    # chat_window.pack(fill="x")
    chat_window.grid(columnspan=2)

    q_button = ttk.Button(main_frame, text="Quit")
    q_button.grid(row=4, column=1)
    q_button['command'] = (lambda: quit_program(mqtt_client))

    # Create an MQTT connection
    my_delegate = MyDelegate(chat_window)
    mqtt_client = com.MqttClient(my_delegate)
    mqtt_client.connect(pc, robit)
    # mqtt_client.connect(my_name, team_member_name, "35.194.247.175")  # Off campus IP address of a GCP broker

    root.mainloop()


def send_message(mqtt_client, my_name, chat_window, msg_entry):
    #   Writes a given message to a chat window under a given name.
    msg = msg_entry.get()
    msg_entry.delete(0, 'end')
    chat_window["text"] += "\nMe: " + msg
    mqtt_client.send_message("on_chat_message", [my_name + ": " + msg])


def quit_program(mqtt_client):
    #   Closes the chat window.
    if mqtt_client:
        mqtt_client.close()
    exit()



