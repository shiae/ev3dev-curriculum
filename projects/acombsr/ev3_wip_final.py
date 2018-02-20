import mqtt_remote_method_calls as com
import ev3dev.ev3 as ev3
import time
import robot_controller as controller


class MyDelegate(object):
    def __init__(self):
        self.running = True


def main():
    my_delegate = MyDelegate()
    robot = controller.Snatch3r()
    mqtt_client = com.MqttClient(robot)
    mqtt_client.connect_to_pc()
    while my_delegate.running:
        time.sleep(.01)


def followLine(robot):
    ev3.Sound.speak("Follow a line").wait()
    white_level = 70
    black_level = 70

    while True:
        command_to_run = input(
            "Enter w (white), b (black), f (follow), or q (for quit): ")
        if command_to_run == 'w':
            print("Calibrate the white light level")
            print("New white level is {}.".format(white_level))
        elif command_to_run == 'b':
            print("Calibrate the black light level")

            print("New black level is {}.".format(black_level))
        elif command_to_run == 'f':
            print("Follow the line until the touch sensor is pressed.")
            follow_the_line(robot, white_level, black_level)
        elif command_to_run == 'q':
            break
        else:
            print(command_to_run,
                  "is not a known command. Please enter a valid choice.")

    print("Goodbye!")
    ev3.Sound.speak("Goodbye").wait()
    robot.shutdown()


def follow_the_line(robot, white_level, black_level):
    while not robot.touch_sensor.is_pressed:
        robot.drive(200, 200)
        while robot.color_sensor.reflected_light_intensity < black_level:
            time.sleep(.01)
        while robot.color_sensor.reflected_light_intensity > white_level:
            robot.turn_degrees(10, 200)

    robot.stop()
    ev3.Sound.speak("Done")


main()
