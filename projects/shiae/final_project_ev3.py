"""


"""

import ev3dev.ev3 as ev3
import time
import robot_controller as robo
import mqtt_remote_method_calls as com
robit = robo.Snatch3r()


class MyDelegate(object):
    def __init__(self):
        self.robot = robo.Snatch3r()
        self.mqtt_client = None  # To be set later.

    def speak_ev3(self):
        print("--------------------------------------------")
        print(" Speak ev3")
        print("--------------------------------------------")
        ev3.Sound.speak('bark bark')


def main():
    # print("--------------------------------------------")
    # print(" Calibrating")
    # print("--------------------------------------------")
    my_delegate = MyDelegate()
    mqtt_client = com.MqttClient(my_delegate)
    mqtt_client.connect_to_pc()
    robit.loop_forever()
    # robit.arm_calibration()
    # friend_tracking()
    # shake()
    # mqtt_client = com.MqttClient(robit)
    # mqtt_client.connect_to_pc()
    # robit.loop_forever()  # Calls a function that has a while True: loop within
    # # it to avoid letting the program end.


def friend_tracking():
    print("--------------------------------------------")
    print(" Friend tracking")
    print("--------------------------------------------")
    print("Press the touch sensor to exit this program.")
    # current_distance = robit.beacon_seeker.distance
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
            while robit.pixy.value(1) < 150 and robit.touch_sensor.is_pressed is False:
                time.sleep(.01)
        elif x > 170:
            robit.turn(-turn_speed, -turn_speed)
            while robit.pixy.value(1) > 170 and robit.touch_sensor.is_pressed is False:
                time.sleep(.01)
        else:
            robit.stop()
            time.sleep(2)
            # if current_distance == -128:
            #     print("where are you?")
            # elif current_distance > 10:
            #     robit.drive(forward_speed, forward_speed)
            #     time.sleep(3)
            # else:
            #     robit.stop()
            #     ev3.Sound.speak("Woof!")

        time.sleep(0.25)

    robit.shutdown()


def shake():
    print("--------------------------------------------")
    print(" Shake")
    print("--------------------------------------------")

    ev3.Sound.speak("shake")

    while not robit.touch_sensor.is_pressed:
        if robit.ir_sensor.proximity < 7:
            robit.shake()
    print("Exit Shake")


main()
