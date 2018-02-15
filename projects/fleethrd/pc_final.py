
import tkinter
from tkinter import ttk
import mqtt_remote_method_calls as com
import math
import random


class MyDelegate(object):

    def __init__(self):
        self.settings = []

    def receive_settings(self, settings):
        self.settings = settings


def main():
    my_delegate = MyDelegate()
    mqtt_client = com.MqttClient(my_delegate)
    mqtt_client.connect_to_ev3()
    root = tkinter.Tk()
    gui(root, mqtt_client)
    root.mainloop()
    random.randint(0, 3)


def gui(root, mqtt_client):
    root.title("Enigma")

    main_frame = ttk.Frame(root)
    main_frame.grid()

    control_variable_0 = tkinter.StringVar(root)
    OPTION_TUPLE = ("a", "b", "c", "d")
    optionmenu_widget = tkinter.OptionMenu(root,
                                           control_variable_0, *OPTION_TUPLE)
    optionmenu_widget.grid(row= 2,column=0)

    control_variable_1 = tkinter.StringVar(root)
    optionmenu_widget_1 = tkinter.OptionMenu(root,
                                           control_variable_1, *OPTION_TUPLE)
    optionmenu_widget_1.grid(row=2, column=1)

    control_variable_2 = tkinter.StringVar(root)
    optionmenu_widget_2 = tkinter.OptionMenu(root,
                                           control_variable_2, *OPTION_TUPLE)
    optionmenu_widget_2.grid(row=2, column=2)

    guess_button = ttk.Button(main_frame, text='guess')
    guess_button.grid(row=0, column=2)
    guess_button['command'] = lambda: send_guess(mqtt_client, control_variable_0,
                                                 control_variable_1, control_variable_2)

    reset_button = ttk.Button(main_frame, text='new marching order')
    reset_button.grid(row=1, column=2)
    reset_button['command'] = lambda: marching_orders(mqtt_client)

    reset_settings_button = ttk.Button(main_frame, text='reset settings')
    reset_settings_button.grid(row=2, column=2)
    reset_settings_button['command'] = lambda: reset_settings(mqtt_client)


def marching_orders(mqtt_client):
    data = ['a', 'a', 'a']
    settings = ['a', 'a', 'a']
    generate(data)
    print('message', data)
    generate(settings)
    enigma(mqtt_client, data, settings)


def enigma(mqtt_client, data, settings):
    x = [2, 0, 1, 3]
    y = [3, 2, 1, 0]
    z = [1, 3, 2, 0]
    r = [2, 3, 0, 1]
    wheels = [0, x, y, z, r]
    mqtt_client.send_message("receive_settings", [settings])
    set_up(settings, wheels)
    encryption(data, wheels)
    mqtt_client.send_message("receive_data", [data])
    print('enciphered', data)


def set_up(settings, wheels):
    letters_to_numbers(settings)
    for k in range(len(settings)):
        for j in range(settings[k]):
            rotation(wheels[k+1])
    numbers_to_letters(settings)


def encryption(data, wheels):
    letters_to_numbers(data)
    system_rotation(wheels)
    data[0] = wheels[1].index(wheels[2].index(wheels[3].index(wheels[4][wheels[3][wheels[2][wheels[1][data[0]]]]])))
    system_rotation(wheels)
    data[1] = wheels[1].index(wheels[2].index(wheels[3].index(wheels[4][wheels[3][wheels[2][wheels[1][data[1]]]]])))
    system_rotation(wheels)
    data[2] = wheels[1].index(wheels[2].index(wheels[3].index(wheels[4][wheels[3][wheels[2][wheels[1][data[2]]]]])))
    numbers_to_letters(data)


def system_rotation(wheels):
    rotation(wheels[1])
    if wheels[0] == 1:
        rotation(wheels[2])
    elif wheels[0] == 2:
        rotation(wheels[3])
    wheels[0] += 1


def rotation(wheel):
    temp = wheel[0]
    for k in range(len(wheel) - 1):
        if wheel[k + 1] > 0:
            wheel[k] = wheel[k + 1] - 1
        else:
            wheel[k] = 3
    if temp > 0:
        wheel[3] = temp - 1
    else:
        wheel[3] = 3


def letters_to_numbers(data):
    for k in range(len(data)):
        if data[k] == 'a':
            data[k] = 0
        elif data[k] == 'b':
            data[k] = 1
        elif data[k] == 'c':
            data[k] = 2
        elif data[k] == 'd':
            data[k] = 3


def numbers_to_letters(data):
    for k in range(len(data)):
        if data[k] == 0:
            data[k] = 'a'
        elif data[k] == 1:
            data[k] = 'b'
        elif data[k] == 2:
            data[k] = 'c'
        elif data[k] == 3:
            data[k] = 'd'


def send_guess(mqtt_client, guess_0, guess_1, guess_2):
    guess = []
    guess.append(guess_0.get())
    guess.append(guess_1.get())
    guess.append(guess_2.get())
    print(guess)
    mqtt_client.send_message("guess_data", [guess])


def generate(list):
    for k in range(len(list)):
        list[k] = random.randint(0,3)
    numbers_to_letters(list)


def reset_settings(mqtt_client):
    mqtt_client.send_message("reset_settings")


main()
