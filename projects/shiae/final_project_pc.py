
# functions: 5-20 lines of code
#

import tkinter
from tkinter import ttk
# import time
# import mqtt_remote_method_calls as com


def main():
    # command()
    root = tkinter.Tk()

    frame1 = ttk.Frame(root, padding=30)
    frame1.grid()

    hello_button = ttk.Button(frame1, text="Hello!")
    hello_button['command'] = (lambda: print("Hello!"))
    hello_button.grid()

    root.mainloop()

# def command():



main()

