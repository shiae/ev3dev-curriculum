
# functions: 5-20 lines of code
#

import tkinter
from tkinter import ttk
# import time
# import mqtt_remote_method_calls as com


# class MyDelegate(object):
#     #   Creates an object which can write a message to a shared chat board.
#     def __init__(self, label):
#         self.label = label

    # def on_chat_message(self, message):
    #     self.label["text"] += "\n" + message


def main():
    command()


def command():
    root = tkinter.Tk()
    frame1 = ttk.Frame(root, padding=20)
    frame1.grid()

    root.mainloop()


main()

