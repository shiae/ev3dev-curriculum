"""
My final project turns the ev3 robot into a dog, who I call Robit. Robit can
speak, come, sit, fetch, and shake.

This file was designed to be run on the ev3. It receives messages from the
PC and executes them.

Author: Allison Shi, February 2018
"""

import ev3dev.ev3 as ev3
import time
import robot_controller as robo
import mqtt_remote_method_calls as com


class MyDelegate(object):
    """ Creates a delegate to receive messages from the PC"""
    def __init__(self):
        self.robot = robo.Snatch3r()
        self.mqtt_client = None  # To be set later.

    def speak(self):
        """ Robit will say 'bark bark'"""
        print("--------------------------------------------")
        print(" Speak")
        print("--------------------------------------------")
        ev3.Sound.speak('bark bark').wait()

    def sit(self):
        """Robit's motors will stop"""
        print("--------------------------------------------")
        print(" Sit")
        print("--------------------------------------------")
        robit = robo.Snatch3r()
        robit.stop()

    def shake(self):
        """ When Robit senses something in front of his IR sensor, his arm
        will move up and down."""
        print("--------------------------------------------")
        print(" Shake")
        print("--------------------------------------------")
        ev3.Sound.speak("shake").wait()
        robit = robo.Snatch3r()
        while not robit.touch_sensor.is_pressed:
            if robit.ir_sensor.proximity < 2:
                robit.shake()
        print("Exit Shake")

    def fetch(self):
        """Robit will look for and retrieve his toy, but will not return it
        to you--he will instead start running in circles."""
        print("--------------------------------------------")
        print(" Fetch")
        print("--------------------------------------------")
        print("Press the touch sensor to exit this program.")
        robit = robo.Snatch3r()
        robit.pixy.mode = "SIG1"
        turn_speed = 100
        forward_speed = 300
        while not robit.touch_sensor.is_pressed:

            x = robit.pixy.value(1)
            y = robit.pixy.value(2)
            width = robit.pixy.value(3)
            height = robit.pixy.value(4)
            area = width * height
            close_enough = \
                7489213479018234709812374092183740921834709128347012938471239084712903847123908471239847

            print("(X, Y)=({}, {})".format(x, y))

            if x < 150:
                robit.turn(turn_speed, turn_speed)
                while robit.pixy.value(
                        1) < 150 and robit.touch_sensor.is_pressed is False:
                    time.sleep(.01)
            elif x > 170:
                robit.turn(-turn_speed, -turn_speed)
                while robit.pixy.value(
                        1) > 170 and robit.touch_sensor.is_pressed is False:
                    time.sleep(.01)
            else:
                robit.stop()
                if area > close_enough:
                    robit.drive(forward_speed, forward_speed)
                    time.sleep(4)
                else:
                    robit.stop()
                    ev3.Sound.speak("Wuff!").wait()
                    robit.arm_up()
                    time.sleep(2)
                    robit.turn_degrees(180, turn_speed)
                    robit.drive(forward_speed, forward_speed - 100)
                    time.sleep(5)

            time.sleep(0.25)

        robit.shutdown()

    def come(self):
        """Robit will look for his toy and come to it."""
        print("--------------------------------------------")
        print(" Come")
        print("--------------------------------------------")
        print("Press the touch sensor to exit this program.")
        robit = robo.Snatch3r()
        ev3.Sound.speak("Come").wait()
        robit.pixy.mode = "SIG1"
        turn_speed = 100
        forward_speed = 300
        while not robit.touch_sensor.is_pressed:

            x = robit.pixy.value(1)
            y = robit.pixy.value(2)
            width = robit.pixy.value(3)
            height = robit.pixy.value(4)
            area = width * height
            close_enough = 300

            print("(X, Y)=({}, {})".format(x, y), width, height, area)

            if x < 150:
                robit.turn(turn_speed, turn_speed)
                while robit.pixy.value(
                        1) < 150 and robit.touch_sensor.is_pressed is False:
                    time.sleep(.01)
            elif x > 170:
                robit.turn(-turn_speed, -turn_speed)
                while robit.pixy.value(
                        1) > 170 and robit.touch_sensor.is_pressed is False:
                    time.sleep(.01)
            else:
                robit.stop()
                if 0 < area < close_enough:
                    robit.drive(forward_speed, forward_speed)
                    time.sleep(3)
                else:
                    robit.stop()
                    ev3.Sound.speak("Wuff!").wait()
                    print("woof")
                    time.sleep(2)

            time.sleep(0.25)

        robit.shutdown()


def main():
    my_delegate = MyDelegate()
    mqtt_client = com.MqttClient(my_delegate)
    mqtt_client.connect_to_pc()
    robit = robo.Snatch3r()
    assert robit.pixy
    assert robit.color_sensor
    print("--------------------------------------------")
    print(" Calibrating")
    print("--------------------------------------------")
    robit.arm_calibration()
    picked_up = 80
    if robit.color_sensor.reflected_light_intensity > picked_up:
        mqtt_client.send_message("love")
    robit.loop_forever()


main()
