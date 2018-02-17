
import mqtt_remote_method_calls as com

import ev3dev.ev3 as ev3
import time
import robot_controller as robo
robot = robo.Snatch3r() # yes, a global variable because I need it in many
# places


class MyDelegate(object):

    def __init__(self):
        self.running = True
        self.data = []
        self.settings = []
        self.guess = []
        self.has_settings = False
        self.win = False
        self.waiting_on_news = False

    def receive_data(self, data):
        self.data = data
        data_copy = []
        print("received", data)
        if len(self.settings) == 3:
            for k in range(len(self.settings)):
                data_copy.append(data[k])
            letters_to_numbers(data_copy)
            letters_to_numbers(self.settings)
            decryption(self.settings, data_copy)
            numbers_to_letters(data_copy)
            numbers_to_letters(self.settings)
            print("guessed", data_copy)
            process_data(data_copy)
            self.win = return_home(data_copy)
            if self.win:
                time.sleep(10)
                return_home(data_copy)
            self.waiting_on_news = True
            ev3.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.AMBER)
            ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.AMBER)
            while self.waiting_on_news is True:
                time.sleep(.01)

    def guess_data(self, guess):
        self.guess = guess
        self.settings = bombe(self.data, self.guess)
        print(self.settings)
        ev3.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.RED)
        ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.RED)
        self.has_settings = True
        while self.has_settings:
            time.sleep(.01)

    def reset_settings(self):
        self.settings = []


def main():
    my_delegate = MyDelegate()
    mqtt_client = com.MqttClient(my_delegate)
    mqtt_client.connect_to_pc()
    btn = ev3.Button()
    btn.on_up = lambda state: handle_up(state, mqtt_client, my_delegate)
    btn.on_down = lambda state: handle_down(state, mqtt_client, my_delegate)
    while my_delegate.running:
        btn.process()
        time.sleep(.01)



def bombe(data, guess):
    letters_to_numbers(data)
    for k in range(4):
        # time.sleep(1)
        for j in range(4):
            # time.sleep(1)
            for i in range(4):
                # time.sleep(1)
                settings = [k, j, i]
                tester = []
                for z in range(len(data)):
                    tester.append(data[z])
                decryption(settings, tester)
                numbers_to_letters(tester)
                if tester == guess:
                    numbers_to_letters(settings)
                    return settings
    return []


def decryption(settings, data):
    x = [2, 0, 1, 3]
    y = [3, 2, 1, 0]
    z = [1, 3, 2, 0]
    r = [2, 3, 0, 1]
    wheels = [0, x, y, z, r]
    set_up(settings, wheels)
    system_rotation(wheels)
    data[0] = wheels[1].index(wheels[2].index(wheels[3].index(wheels[4].index(wheels[3][wheels[2][wheels[1][data[0]]]]))))
    system_rotation(wheels)
    data[1] = wheels[1].index(wheels[2].index(wheels[3].index(wheels[4].index(wheels[3][wheels[2][wheels[1][data[1]]]]))))
    system_rotation(wheels)
    data[2] = wheels[1].index(wheels[2].index(wheels[3].index(wheels[4].index(wheels[3][wheels[2][wheels[1][data[2]]]]))))


def set_up(settings, wheels):
    for k in range(len(settings)):
        for j in range(settings[k]):
            rotation(wheels[k+1])


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


def handle_up(state, mqtt_client, my_delegate):
    if state and my_delegate.has_settings:
        print("up button was pressed")
        mqtt_client.send_message("receive-settings", [my_delegate.settings])
        my_delegate.freeze = False


def process_data(data):
    speed = 200
    if data[0] == 'd':
        time.sleep(10)
    elif data[0] == 'a':
        robot.follow_line('blue')
    elif data[0] == 'b':
        robot.follow_line('blue')
        robot.turn_degrees(-30, speed)
        robot.follow_line('red')
    elif data[0] == 'c':
        robot.follow_line('blue')
        robot.turn(30, speed)
        robot.follow_line('green')

def return_home(data):
    speed = 200
    robot.turn_degrees(180, speed)
    if data[0] == 'a':
        robot.follow_line('black')
    elif data[0] == 'b':
        robot.follow_line('blue')
        robot.turn_degrees(30, speed)
        robot.follow_line('black')
    elif data[0] == 'c':
        robot.follow_line('blue')
        robot.turn_degrees(-30, speed)
        robot.follow_line('black')


def handle_down(state, mqtt_client, my_delegate):
    if state and my_delegate.waiting_on_news:
        mqtt_client.send_message(
            "receive_news_on_war", [my_delegate.waiting_on_news])
        my_delegate.waiting_on_news = False


main()
