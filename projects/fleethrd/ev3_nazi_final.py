
import mqtt_remote_method_calls as com

import ev3dev.ev3 as ev3
import time
import robot_controller as robo


class MyDelegate(object):
    """handles function calls from the pc"""

    def __init__(self):
        self.running = True
        self.data = ['a', 'a', 'a']
        self.settings = ['a', 'a', 'a']
        self.foiled_by_damn_allies = False
        self.robot = robo.Snatch3r()

    def receive_data(self, data):
        """receives data figures out what to do with it"""
        self.data = data
        decryption(self.settings, self.data)
        self.foiled_by_damn_allies = process_data(self.data, self)
        return_home(self.foiled_by_damn_allies, self.data, self)

    def receive_settings(self, settings):
        """receives settings"""
        self.settings = settings

    def shutdown(self):
        self.running = False
        self.robot.shutdown()


def main():
    my_delegate = MyDelegate()
    mqtt_client = com.MqttClient(my_delegate)
    mqtt_client.connect_to_pc()
    while my_delegate.running:
        time.sleep(.01)


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
    print(data)


def set_up(settings, wheels):
    """sets the wheels up based on the given settings"""
    letters_to_numbers(settings)
    for k in range(len(settings)):
        for j in range(settings[k]):
            rotation(wheels[k+1])
    numbers_to_letters(settings)


def system_rotation(wheels):
    """rotates the wheels based on a set algorithm"""
    rotation(wheels[1])
    if wheels[0] == 1:
        rotation(wheels[2])
    elif wheels[0] == 2:
        rotation(wheels[3])
    wheels[0] += 1


def rotation(wheel):
    """rotates a single wheel"""
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
    """converts a list of letters into a list of numbers"""
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
    """converts a list of numbers into a list of numbers"""
    for k in range(len(data)):
        if data[k] == 0:
            data[k] = 'a'
        elif data[k] == 1:
            data[k] = 'b'
        elif data[k] == 2:
            data[k] = 'c'
        elif data[k] == 3:
            data[k] = 'd'


def process_data(data, my_delegate):
    """figures out how to move the my_delegate.robot based on the given data"""
    speed = 200
    foiled = False
    if data[0] == 'd':
        time.sleep(10)
    else:
        if data[2] == 'a':
            my_delegate.robot.follow_line('blue')
            if data[0] == 'a':
                time.sleep(5)
            elif data[0] == 'b':
                my_delegate.robot.turn_degrees(150, speed)
                foiled = my_delegate.robot.follow_line('red')
            elif data[0] == 'c':
                my_delegate.robot.turn_degrees(-150, speed)
                foiled = my_delegate.robot.follow_line('green')
        elif data[2] == 'b':
            my_delegate.robot.turn_degrees(120, speed)
            my_delegate.robot.follow_line('red')
            if data[0] == 'a':
                my_delegate.robot.turn_degrees(-150, speed)
                foiled = my_delegate.robot.follow_line('blue')
            elif data[0] == 'b':
                time.sleep(5)
            elif data[0] == 'c':
                my_delegate.robot.turn_degrees(150, speed)
                foiled = my_delegate.robot.follow_line('green')
        elif data[2] == 'c':
            my_delegate.robot.turn_degrees(-120, speed)
            my_delegate.robot.follow_line('green')
            if data[0] == 'a':
                my_delegate.robot.turn_degrees(150, speed)
                foiled = my_delegate.robot.follow_line('blue')
            elif data[0] == 'b':
                my_delegate.robot.turn_degrees(-150, speed)
                foiled = my_delegate.robot.follow_line('red')
            elif data[0] == 'c':
                time.sleep(5)
        elif data[2] == 'd':
            if data[0] == 'a':
                foiled = my_delegate.robot.follow_line('blue')
            elif data[0] == 'b':
                my_delegate.robot.turn_degrees(120, speed)
                foiled = my_delegate.robot.follow_line('red')
            elif data[0] == 'c':
                my_delegate.robot.turn_degrees(-120, speed)
                foiled = my_delegate.robot.follow_line('green')
    return foiled


def return_home(foiled, data, my_delegate):
    """returns to the my_delegate.robot to start"""
    speed = 200
    if my_delegate.robot.color_sensor.color != \
            my_delegate.robot.color_sensor.COLOR_WHITE:
        figuring_out_how_to_get_home(data[2], my_delegate)
    else:
        figuring_out_where_i_ended_up(data, my_delegate)
    if foiled:
        my_delegate.robot.follow_line('blue')
        time.sleep(10)
        my_delegate.robot.turn_degrees(180, speed)
        my_delegate.robot.follow_line('black')
        my_delegate.robot.turn_degrees(180, speed)


def figuring_out_where_i_ended_up(data, my_delegate):
    """figures out roughly where the my_delegate.robot ended up"""
    speed = 200
    if data[2] == 'd':
        my_delegate.robot.turn_degrees(180, speed)
        my_delegate.robot.follow_line('black')
        if data[0] == 'a':
            my_delegate.robot.turn_degrees(180, speed)
        elif data[0] == 'b':
            my_delegate.robot.turn_degrees(30, speed)
        elif data[0] == 'c':
            my_delegate.robot.turn_degrees(-30, speed)
    elif data[2] == 'a':
        my_delegate.robot.turn_degrees(180, speed)
        my_delegate.robot.follow_line('blue')
        figuring_out_how_to_get_home(data[0], my_delegate)
    elif data[2] == 'b':
        my_delegate.robot.turn_degrees(180, speed)
        my_delegate.robot.follow_line('red')
        figuring_out_how_to_get_home(data[0], my_delegate)
    elif data[2] == 'c':
        my_delegate.robot.turn_degrees(180, speed)
        my_delegate.robot.follow_line('green')
        figuring_out_how_to_get_home(data[0], my_delegate)


def figuring_out_how_to_get_home(route, my_delegate):
    """figures out how to get the my_delegate.robot back to start"""
    speed = 200
    if my_delegate.robot.color_sensor.color == \
            my_delegate.robot.color_sensor.COLOR_BLUE:
        if route == 'a':
            my_delegate.robot.turn_degrees(180, speed)
            my_delegate.robot.follow_line('black')
            my_delegate.robot.turn_degrees(180, speed)
        elif route == 'b':
            my_delegate.robot.turn_degrees(-150, speed)
            my_delegate.robot.follow_line('black')
            my_delegate.robot.turn_degrees(180, speed)
        elif route == 'c':
            my_delegate.robot.turn_degrees(150, speed)
            my_delegate.robot.follow_line('black')
            my_delegate.robot.turn_degrees(180, speed)
        elif route == 'd':
            my_delegate.robot.turn_degrees(180, speed)
            my_delegate.robot.follow_line('black')
            my_delegate.robot.turn_degrees(180, speed)
    elif my_delegate.robot.color_sensor.color == \
            my_delegate.robot.color_sensor.COLOR_RED:
        if route == 'a':
            my_delegate.robot.turn_degrees(150, speed)
            my_delegate.robot.follow_line('black')
            my_delegate.robot.turn_degrees(30, speed)
        elif route == 'b':
            my_delegate.robot.turn_degrees(180, speed)
            my_delegate.robot.follow_line('black')
            my_delegate.robot.turn_degrees(30, speed)
        elif route == 'c':
            my_delegate.robot.turn_degrees(-150, speed)
            my_delegate.robot.follow_line('black')
            my_delegate.robot.turn_degrees(30, speed)
        elif route == 'd':
            my_delegate.robot.turn_degrees(180, speed)
            my_delegate.robot.follow_line('black')
            my_delegate.robot.turn_degrees(30, speed)
    elif my_delegate.robot.color_sensor.color == \
            my_delegate.robot.color_sensor.COLOR_GREEN:
        if route == 'a':
            my_delegate.robot.turn_degrees(-150, speed)
            my_delegate.robot.follow_line('black')
            my_delegate.robot.turn_degrees(-30, speed)
        elif route == 'b':
            my_delegate.robot.turn_degrees(180, speed)
            my_delegate.robot.follow_line('black')
            my_delegate.robot.turn_degrees(-30, speed)
        elif route == 'c':
            my_delegate.robot.turn_degrees(150, speed)
            my_delegate.robot.follow_line('black')
            my_delegate.robot.turn_degrees(-30, speed)
        elif route == 'd':
            my_delegate.robot.turn_degrees(180, speed)
            my_delegate.robot.follow_line('black')
            my_delegate.robot.turn_degrees(-30, speed)


main()
