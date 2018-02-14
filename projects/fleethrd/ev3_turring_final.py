
import mqtt_remote_method_calls as com

import ev3dev.ev3 as ev3
import time


class MyDelegate(object):

    def __init__(self):
        self.running = True
        self.data = []
        self.settings = []
        self.guess = []

    def receive_data(self, data):
        self.data = data
        print(data)

    def guess_data(self, guess):
        print(guess)
        self.guess = guess
        self.settings = bombe(self.data, self.settings, self.guess)
        print(self.settings)

    def receive_settings(self, settings):
        print ('settings unknown')

def main():
    my_delegate = MyDelegate()
    mqtt_client = com.MqttClient(my_delegate)
    mqtt_client.connect_to_pc()
    while my_delegate.running:
        time.sleep(.01)


def bombe(data, settings, guess):
    letters_to_numbers(data)
    for k in range(4):
        time.sleep(1)
        for j in range(4):
            time.sleep(1)
            for i in range(4):
                time.sleep(1)
                settings = [k, j, i]
                tester = []
                for z in range(len(data)):
                    tester.append(data[z])
                decryption(settings, tester)
                numbers_to_letters(tester)
                if tester == guess:
                    numbers_to_letters(settings)
                    return settings


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



main()
