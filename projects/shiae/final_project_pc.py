
# functions: 5-20 lines of code
#

import tkinter
from tkinter import ttk
import mqtt_remote_method_calls as com
mqtt_client = com.MqttClient()
mqtt_client.connect_to_ev3()


def main():
    speak_button()


def speak_button():
    root = tkinter.Tk()

    frame1 = ttk.Frame(root, padding=30)
    frame1.grid()

    hello_button = ttk.Button(frame1, text="Speak")
    hello_button['command'] = (lambda: speak_pc())
    hello_button.grid()

    root.mainloop()


def speak_pc():
    print("--------------------------------------------")
    print(" Speak PC")
    print("--------------------------------------------")
    mqtt_client.send_message("speak_ev3")


main()

