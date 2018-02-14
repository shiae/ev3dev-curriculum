"""


"""

import ev3dev.ev3 as ev3
import time
# import tkinter
# from tkinter import ttk
import robot_controller as robo
robit = robo.Snatch3r()


def main():
    # friend_tracking()
    shake()
    # mqtt_client = com.MqttClient(robit)
    # mqtt_client.connect_to_pc()
    # robit.loop_forever()  # Calls a function that has a while True: loop within
    # # it to avoid letting the program end.


def friend_tracking():
    print("--------------------------------------------")
    print(" Friend tracking")
    print("--------------------------------------------")
    print("Press the touch sensor to exit this program.")
    robit.pixy.mode = "SIG1"
    turn_speed = 100
    forward_speed = 300
    robit.pixy.mode = "SIG1"
    while not robit.touch_sensor.is_pressed:

        x = robit.pixy.value(1)
        y = robit.pixy.value(2)
        # width = robit.pixy.value(3)
        # height = robit.pixy.value(4)
        # area = width * height

        print("(X, Y)=({}, {})".format(x, y))

        if x < 150:
            robit.turn(turn_speed, turn_speed)
            while robit.pixy.value(1) < 150 and \
                            robit.touch_sensor.is_pressed is False:
                time.sleep(.01)
        elif x > 170:
            robit.turn(-turn_speed, -turn_speed)
            while robit.pixy.value(1) > 170 and \
                            robit.touch_sensor.is_pressed is False:
                time.sleep(.01)
        else:
            robit.drive(forward_speed, forward_speed)

        time.sleep(0.25)

    robit.shutdown()


def shake():
    print("--------------------------------------------")
    print(" Shake")
    print("--------------------------------------------")

    while not robit.touch_sensor.is_pressed:
        if robit.ir_sensor.proximity < 10:
            robit.arm_up()
            time.sleep(1)
            robit.arm_down()
            time.sleep(1)
    time.sleep(0.01)


main()
