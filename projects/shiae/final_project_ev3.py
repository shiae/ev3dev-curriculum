"""


"""

import ev3dev.ev3 as ev3
import time
# import tkinter
# from tkinter import ttk
import robot_controller as robo
robit = robo.Snatch3r()
import mqtt_remote_method_calls as com


# class MyDelegate:
#     def __init__(self):
#
#

my_delegate = MyDelegate()
mqtt_client = com.MqttClient(my_delegate)
my_delegate.mqtt_client = mqtt_client
mqtt_client.connect_to_pc()

def main():
    robit.arm_calibration()
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
    # forward_speed = 300
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
            robit.stop()
            ev3.Sound.speak("Friend!")
            time.sleep(2)

        time.sleep(0.25)

    robit.shutdown()


def shake():
    print("--------------------------------------------")
    print(" Shake")
    print("--------------------------------------------")

    ev3.Sound.speak("shake")

    robit.arm_motor.run_to_abs_pos(position_sp=0, speed_sp=robit.MAX_SPEED)
    robit.arm_motor.wait_while(
        ev3.Motor.STATE_RUNNING)
    # robit.arm_motor.run_forever(speed_sp=robit.MAX_SPEED)
    # time.sleep(4)

    if robit.ir_sensor.proximity < 10:
        robit.shake()

main()
