"""


"""

# import ev3dev.ev3 as ev3
import time
# import tkinter
# from tkinter import ttk
import robot_controller as robo


def main():
    robit = robo.Snatch3r()
    # mqtt_client = com.MqttClient(robit)
    # mqtt_client.connect_to_pc()
    # robit.loop_forever()  # Calls a function that has a while True: loop within
    # # it to avoid letting the program end.

    print("--------------------------------------------")
    print(" Friend tracking")
    print("--------------------------------------------")
    print("Press the touch sensor to exit this program.")

    robit.pixy.mode = "SIG1"
    turn_speed = 100

    while not robit.touch_sensor.is_pressed:

        x = robit.pixy.value(1)
        y = robit.pixy.value(2)

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

        time.sleep(0.25)

    robit.shutdown()


main()
