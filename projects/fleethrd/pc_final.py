# the pc part of the final that randomly generates a message and settings to
# encrypt.  It sends data to the robot and receives data from it as well.
# Some features are commented out or unused as originally the plan was to have
# two robots but that fell through at midnight

import tkinter
from tkinter import ttk
import mqtt_remote_method_calls as com
import random
import time


class MyDelegate(object):
    """handles function calls from the robots"""

    def __init__(self, display, nazi_health, allied_health):
        self.settings = []
        self.display = display
        self.allied_health = 10
        self.nazi_health = 3
        self.nazi_health_display = nazi_health
        self.allied_health_display = allied_health

    def receive_settings(self, settings):
        """receives settings from the turing device and displays them"""
        self.settings = settings
        message_to_display = "{} was received for settings".format(settings)
        self.display.configure(text=message_to_display)

    def receive_news_on_war(self, news):
        """receives news from the turing bot and sets the score based on it"""
        print('it bloody worked')
        if news is True:
            self.nazi_health -= 1
            self.nazi_health_display.configure(text=self.nazi_health)
            if self.nazi_health == 0:
                message_to_display = "Allies Win! Press Exit to Leave Game"
                self.display.configure(text=message_to_display)
                exit()
        else:
            self.allied_health -= 1
            self.allied_health_display.configure(text=self.allied_health)
            if self.allied_health == 0:
                message_to_display = "Nazis Win! Press Exit to Leave Game"
                self.display.configure(text=message_to_display)
                exit()

    def receive_news_one_robot(self, settings, data,
                               data_copy):
        """takes the original data and settings and compares it to the found settings to figure out if the nazis were foiled that turn"""
        print('hey')
        news = False
        if decryption(settings, data) == decryption(self.settings,
                                                    data_copy):
            news = True
        print(data)
        print(data_copy)
        if news is True:
            self.nazi_health -= 1
            self.nazi_health_display.configure(text=self.nazi_health)
            if self.nazi_health == 0:
                message_to_display = "Allies Win! Press Exit to Leave Game"
                self.display.configure(text=message_to_display)
                exit()
        else:
            self.allied_health -= 1
            self.allied_health_display.configure(text=self.allied_health)
            if self.allied_health == 0:
                message_to_display = "Nazis Win! Press Exit to Leave Game"
                self.display.configure(text=message_to_display)
                exit()


def main():
    root = tkinter.Tk()
    gui(root)
    root.mainloop()


def gui(root):
    """initiates all of the gui and mqtt"""
    root.title("Enigma")

    main_frame = ttk.Frame(root)
    main_frame.grid()

    control_variable_0 = tkinter.StringVar(root)
    option_tuple = ("a", "b", "c", "d")
    optionmenu_widget = tkinter.OptionMenu(root,
                                           control_variable_0, *option_tuple)
    optionmenu_widget.grid(row=1, column=0)

    control_variable_1 = tkinter.StringVar(root)
    optionmenu_widget_1 = tkinter.OptionMenu(root,
                                           control_variable_1, *option_tuple)
    optionmenu_widget_1.grid(row=2, column=0)

    control_variable_2 = tkinter.StringVar(root)
    optionmenu_widget_2 = tkinter.OptionMenu(root,
                                           control_variable_2, *option_tuple)
    optionmenu_widget_2.grid(row=3, column=0)

    guess_button = ttk.Button(main_frame, text='Guess Message')
    guess_button.grid(row=2, column=1)
    guess_button['command'] = lambda: send_guess(mqtt_client,
                                                 control_variable_0,
                                                 control_variable_1, control_variable_2)

    reset_settings_button = ttk.Button(main_frame, text='Reset Settings')
    reset_settings_button.grid(row=3, column=1)
    reset_settings_button['command'] = lambda: reset_settings(mqtt_client)

    display = ttk.Label(main_frame, text="--")
    display.grid(row=0, column=1)

    nazi_health_label = ttk.Label(main_frame, text='Nazi Health')
    nazi_health_label.grid(row=0, column=0)

    nazi_health = ttk.Label(main_frame, text='3')
    nazi_health.grid(row=1, column=0)

    allied_health_label = ttk.Label(main_frame, text='Allied Health')
    allied_health_label.grid(row=0, column=2)

    allied_health = ttk.Label(main_frame, text='10')
    allied_health.grid(row=1, column=2)

    shut_down_button = ttk.Button(main_frame, text='Exit Game')
    shut_down_button.grid(row=5, column=2)
    shut_down_button['command'] = lambda: shutdown(mqtt_client)

    start_button = ttk.Button(main_frame, text='Start Game')
    start_button.grid(row=5, column=0)
    start_button['command'] = lambda: start_game(mqtt_client)

    next_orders_button = ttk.Button(main_frame, text='Next Campaign')
    next_orders_button.grid(row=5, column=1)
    next_orders_button['command'] = lambda: marching_orders(mqtt_client)

    guess_label = ttk.Label(main_frame, text="Make Your Guess Below")
    guess_label.grid(row=6, column=1)

    my_delegate = MyDelegate(display, nazi_health, allied_health)
    mqtt_client = com.MqttClient(my_delegate)
    mqtt_client.connect_to_ev3()


def marching_orders(mqtt_client):
    """randomly generates both settings and data for the robots"""
    data = ['a', 'a', 'a']
    settings = ['a', 'a', 'a']
    generate(data)
    print('message', data)
    generate(settings)
    enigma(mqtt_client, data, settings)


def enigma(mqtt_client, data, settings):
    """creates the enigma system and sends encrypted data to the robots"""
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
    """takes the given settings and sets the enigma wheels to those settings"""
    letters_to_numbers(settings)
    for k in range(len(settings)):
        for j in range(settings[k]):
            rotation(wheels[k+1])
    numbers_to_letters(settings)


def encryption(data, wheels):
    """takes a given set of data and set of wheels and encrypts the data"""
    letters_to_numbers(data)
    system_rotation(wheels)
    data[0] = wheels[1].index(wheels[2].index(wheels[3].index(wheels[4][wheels[3][wheels[2][wheels[1][data[0]]]]])))
    system_rotation(wheels)
    data[1] = wheels[1].index(wheels[2].index(wheels[3].index(wheels[4][wheels[3][wheels[2][wheels[1][data[1]]]]])))
    system_rotation(wheels)
    data[2] = wheels[1].index(wheels[2].index(wheels[3].index(wheels[4][wheels[3][wheels[2][wheels[1][data[2]]]]])))
    numbers_to_letters(data)


def system_rotation(wheels):
    """shifts the whole system of wheels based on a set algorithm"""
    rotation(wheels[1])
    if wheels[0] == 1:
        rotation(wheels[2])
    elif wheels[0] == 2:
        rotation(wheels[3])
    wheels[0] += 1


def rotation(wheel):
    """shifts one wheel"""
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
    """converts a list of letters into a list of number"""
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
    """converts a list of numbers into a list of letters"""
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
    """takes an input guess, sends it to the turing bot, and initiates a new move"""
    guess = []
    guess.append(guess_0.get())
    guess.append(guess_1.get())
    guess.append(guess_2.get())
    print(guess)
    mqtt_client.send_message("guess_data", [guess])
    time.sleep(30)
    marching_orders(mqtt_client)


def generate(input_list):
    """randomly generates a list"""
    for k in range(len(input_list)):
        input_list[k] = random.randint(0, 3)
    numbers_to_letters(input_list)


def reset_settings(mqtt_client):
    """sends a message to the turing to reset its enigma settings"""
    mqtt_client.send_message("reset_settings")


def shutdown(mqtt_client):
    """tells the robot to shutdown and then closes the program"""
    mqtt_client.send_message('shutdown', [])
    mqtt_client.close()
    exit()


def start_game(mqtt_client):
    """starts the game by sending out the first set of data"""
    marching_orders(mqtt_client)


def decryption(settings, data):
    """decrypts the given set of encrypted data with the given settings"""
    x = [2, 0, 1, 3]
    y = [3, 2, 1, 0]
    z = [1, 3, 2, 0]
    r = [2, 3, 0, 1]
    wheels = [0, x, y, z, r]
    set_up(settings, wheels)
    letters_to_numbers(data)
    system_rotation(wheels)
    data[0] = wheels[1].index(wheels[2].index(wheels[3].index(wheels[4].index(wheels[3][wheels[2][wheels[1][data[0]]]]))))
    system_rotation(wheels)
    data[1] = wheels[1].index(wheels[2].index(wheels[3].index(wheels[4].index(wheels[3][wheels[2][wheels[1][data[1]]]]))))
    system_rotation(wheels)
    data[2] = wheels[1].index(wheels[2].index(wheels[3].index(wheels[4].index(wheels[3][wheels[2][wheels[1][data[2]]]]))))
    numbers_to_letters(data)
    return data


main()
