
import mqtt_remote_method_calls as com

import ev3dev.ev3 as ev3
import time
import robot_controller as robo
robot = robo.Snatch3r() # yes, a global variable because I need it in many
# places


class MyDelegate(object):

    def __init__(self):
        self.running = True
        self.data = ['a', 'a', 'a']
        self.settings = ['a', 'a', 'a']

    def receive_data(self, data):
        self.data = data
        decryption(self.settings, self.data)
        process_data(self.data)

    def receive_settings(self, settings):
        self.settings = settings

def main():
    my_delegate = MyDelegate()
    mqtt_client = com.MqttClient(my_delegate)
    mqtt_client.connect_to_pc()
    while my_delegate.running:
        time.sleep(.01)


def decryption(settings, data):
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
    print(data)


def set_up(settings, wheels):
    letters_to_numbers(settings)
    for k in range(len(settings)):
        for j in range(settings[k]):
            rotation(wheels[k+1])
    numbers_to_letters(settings)


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


def process_data(data):
    speed = 200
    if data[0] == 'd':
        time.sleep(10)
    else:
        if data[2] == 'a':
            robot.follow_line('blue')
            if data[0] == 'a':
                time.sleep(5)
            elif data[0] == 'b':
                robot.turn_degrees(150, speed)
                robot.follow_line('red')
            elif data[0] == 'c':
                robot.turn_degrees(-150, speed)
                robot.follow_line('green')
        elif data[2] =='b':
            robot.turn_degrees(120, speed)
            robot.follow_line('red')
            if data[0] == 'a':
                robot.turn_degrees(-150, speed)
                robot.follow_line('blue')
            elif data[0] == 'b':
                time.sleep(5)
            elif data[0] == 'c':
                robot.turn_degrees(150, speed)
                robot.follow_line('green')
        elif data[2] =='c':
            robot.turn_degrees(-120, speed)
            robot.follow_line('green')
            if data[0] == 'a':
                robot.turn_degrees(150, speed)
                robot.follow_line('blue')
            elif data[0] == 'b':
                robot.turn_degrees(-150, speed)
                robot.follow_line('red')
            elif data[0] == 'c':
                time.sleep(5)
        else:
            time.sleep(5)


main()
