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
        if(robot.has_moved == True):
            mqtt_client.send_message("on_square_draw", [robot.color,
                                                        robot.x_dir,
                                                        robot.y_dir,
                                                        robot.grid_size])
            robot.has_moved = False
        time.sleep(.01)


main()
