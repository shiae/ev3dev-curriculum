"""
  Library of EV3 robot functions that are useful in many different applications. For example things
  like arm_up, arm_down, driving around, or doing things with the Pixy camera.

  Add commands as needed to support the features you'd like to implement.  For organizational
  purposes try to only write methods into this library that are NOT specific to one tasks, but
  rather methods that would be useful regardless of the activity.  For example, don't make
  a connection to the remote control that sends the arm up if the ir remote control up button
  is pressed.  That's a specific input --> output task.  Maybe some other task would want to use
  the IR remote up button for something different.  Instead just make a method called arm_up that
  could be called.  That way it's a generic action that could be used in any task.
"""

import ev3dev.ev3 as ev3
import time


class Snatch3r(object):
    """Commands for the Snatch3r robot that might be useful in many different programs."""

    def __init__(self):
        #   Creates the variables held by the Snatch3r object.
        self.left_motor = ev3.LargeMotor(ev3.OUTPUT_B)
        self.right_motor = ev3.LargeMotor(ev3.OUTPUT_C)
        self.arm_motor = ev3.MediumMotor(ev3.OUTPUT_A)
        self.touch_sensor = ev3.TouchSensor()
        self.color_sensor = ev3.ColorSensor()
        self.ir_sensor = ev3.InfraredSensor()
        self.beacon_seeker = ev3.BeaconSeeker(channel=1)
        self.pixy = ev3.Sensor(driver_name="pixy-lego")

        self.MAX_SPEED = 900
        self.running = True

        self.facing = 'right'
        self.x_dir = 400
        self.y_dir = 200
        self.color = 5
        self.has_moved = False
        self.grid_size = 0

        assert self.left_motor.connected
        assert self.right_motor.connected
        assert self.arm_motor.connected
        assert self.touch_sensor.connected
        assert self.color_sensor.connected
        assert self.ir_sensor.connected
        assert self.pixy.connected

    def drive_inches(self, inches_target, speed_deg_per_second):
        #   Drives forward a set number of inches given the number of inches
        #  and the speed desired.
        inches_target = inches_target * 90
        self.left_motor.run_to_rel_pos(position_sp=inches_target,
                                       speed_sp=speed_deg_per_second)
        self.right_motor.run_to_rel_pos(position_sp=inches_target,
                                        speed_sp=speed_deg_per_second)
        self.right_motor.wait_while(ev3.Motor.STATE_RUNNING)

    def turn_degrees(self, degrees_to_turn, turn_speed_sp):
        #   Spins the robot around a set number of degrees given the number
        # of degrees and the speed desired.
        degrees_to_turn *= 4.61004
        self.right_motor.run_to_rel_pos(position_sp=-degrees_to_turn,
                                        speed_sp=turn_speed_sp)
        self.left_motor.run_to_rel_pos(position_sp=degrees_to_turn,
                                       speed_sp=turn_speed_sp)
        self.left_motor.wait_while(ev3.Motor.STATE_RUNNING)

    def arm_calibration(self):
        #   The arm motor is set to move up until the touch sensor is
        # pressed. Then the robot beeps, and the arm resets and beeps.
        self.arm_motor.run_forever(speed_sp=self.MAX_SPEED)
        while not self.touch_sensor.is_pressed:
            time.sleep(0.01)
        self.arm_motor.stop(stop_action="brake")
        ev3.Sound.beep().wait()

        arm_revolutions_for_full_range = 14.2
        self.arm_motor.run_to_rel_pos(
            position_sp=-arm_revolutions_for_full_range * 360)
        self.arm_motor.wait_while(ev3.Motor.STATE_RUNNING)

        self.arm_motor.position = 0
        ev3.Sound.beep().wait()

    def arm_up(self):
        #   Moves the arm up until the touch sensor is pressed, then beeps.
        self.arm_motor.run_forever(speed_sp=self.MAX_SPEED)
        while not self.touch_sensor.is_pressed:
            time.sleep(0.01)
        self.arm_motor.stop(stop_action='brake')
        ev3.Sound.beep().wait()

    def arm_down(self):
        #   Moves the
        # arm up until the arm returns to it's lowest position,
        # then beeps.
        self.arm_motor.run_to_abs_pos(position_sp=0, speed_sp=self.MAX_SPEED)
        self.arm_motor.wait_while(
            ev3.Motor.STATE_RUNNING)
        ev3.Sound.beep().wait()

    def shutdown(self):
        #   Stops all motors, sets the leds to green, prints and speaks
        # "goodbye" and then turns itself off.
        self.arm_motor.stop()
        self.left_motor.stop()
        self.right_motor.stop()
        ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.GREEN)
        ev3.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.GREEN)
        print('Goodbye')
        # ev3.Sound.speak('Goodbye').wait()
        self.running = False

    def drive(self, left_speed, right_speed):
        """drives forward for positive values and backwards for negative values"""
        self.left_motor.run_forever(speed_sp=left_speed)
        self.right_motor.run_forever(speed_sp=right_speed)

    def hop(self, grid_size):
        """hops forward for positive values and backwards for negative
        values"""
        print('hop!')
        print(grid_size)
        current_color = 'red'
        self.left_motor.run_to_rel_pos(position_sp=(10*grid_size),
                                       speed_sp=900,
                                       stop_action='brake')
        self.right_motor.run_to_rel_pos(position_sp=(10*grid_size),
                                        speed_sp=900,
                                       stop_action='brake')

        if(self.facing == 'right'):
            self.x_dir += grid_size
        if (self.facing == 'left'):
            self.x_dir -= grid_size
        if (self.facing == 'up'):
            self.y_dir += grid_size
        if (self.facing == 'down'):
            self.y_dir -= grid_size

        current_color = self.color_sensor.color
        self.grid_size = grid_size

        if current_color == 1:
            self.color = 'black'
        if current_color == 2:
            current_color = 'blue'
        if current_color == 3:
            self.color = 'green'
        if current_color == 4:
            self.color = 'yellow'
        if current_color == 5:
            self.color = 'red'
        if current_color == 6:
            self.color = 'white'
        if current_color == 7:
            self.color = 'brown'


        self.has_moved = True
        print("Facing ", self.facing)
        print("X: ", self.x_dir)
        print("Y: ", self.y_dir)

    def rotate_right(self):
        """hops forward for positive values and backwards for negative
        values"""
        print('hop!')
        self.left_motor.run_to_rel_pos(position_sp=400, speed_sp=900,
                                       stop_action='brake')
        self.right_motor.run_to_rel_pos(position_sp=-400, speed_sp=-900,
                                       stop_action='brake')

        print("Facing ", self.facing)

        if (self.facing == 'right'):
            self.facing = 'down'
        elif (self.facing == 'left'):
            self.facing = 'up'
        elif (self.facing == 'up'):
            self.facing = 'right'
        elif (self.facing == 'down'):
            self.facing = 'left'
        print("Facing ", self.facing)


    def rotate_left(self):
        """hops forward for positive values and backwards for negative
        values"""
        print('left!')
        self.left_motor.run_to_rel_pos(position_sp=-400, speed_sp=900,
                                       stop_action='brake')
        self.right_motor.run_to_rel_pos(position_sp=400, speed_sp=900,
                                       stop_action='brake')

        print("Facing ", self.facing)

        if (self.facing == 'right'):
            self.facing = 'up'
        elif(self.facing == 'left'):
            self.facing = 'down'
        elif(self.facing == 'up'):
            self.facing = 'left'
        elif(self.facing == 'down'):
            self.facing = 'right'

        print("Facing ", self.facing)

    def turn(self, left_speed, right_speed):
        """turns left for positive values and right for negative values"""
        print(left_speed)
        print(right_speed)
        self.left_motor.run_forever(speed_sp=-left_speed)
        self.right_motor.run_forever(speed_sp=right_speed)

    def stop(self):
        #   Stops the left and right motors.
        self.right_motor.stop(stop_action='brake')
        self.left_motor.stop(stop_action='brake')

    def loop_forever(self):
        #   Makes sure the robot is running.
        self.running = True

        while self.running:
            time.sleep(0.1)

    def seek_beacon(self):
        """positions the robot to face a beacon object and moves the robot
        towards the beacon to pick it up and set it back down"""
        forward_speed = 300
        turn_speed = 100

        while not self.touch_sensor.is_pressed:
            current_heading = self.beacon_seeker.heading
            current_distance = self.beacon_seeker.distance
            if current_distance == -128:
                print("IR Remote not found. Distance is -128")
                self.stop()
            else:
                if abs(current_heading) < 2:
                    print("On the right heading. Distance: ", current_distance)
                    self.drive(forward_speed, forward_speed)
                    while self.beacon_seeker.distance > 1 and self.touch_sensor.is_pressed is False:
                        time.sleep(0.01)
                    self.stop()
                    return True
                elif abs(current_heading) >= 2 and abs(
                        current_heading) < 10:
                    if current_heading < 0:
                        self.turn(turn_speed, turn_speed)
                        while self.beacon_seeker.heading <= -2:
                            time.sleep(0.01)
                        self.stop()
                    else:
                        self.turn(-turn_speed, -turn_speed)
                        while self.beacon_seeker.heading >= 2:
                            time.sleep(0.01)
                        self.stop()

                else:
                    self.stop()
                    print("Heading too far off")
                    ev3.Sound.speak("Heading too far off").wait()
                    return False

            time.sleep(0.02)
        print("Abandon ship!")
        self.stop()
        return False

    def shake(self):
        """ The arm of the robot moves up for one second, down for one
        second, and then goes to position 0."""
        self.arm_motor.run_forever(speed_sp=self.MAX_SPEED)
        time.sleep(4)

        self.arm_motor.run_forever(speed_sp=-self.MAX_SPEED)
        time.sleep(1)
        self.arm_motor.run_forever(speed_sp=self.MAX_SPEED)
        time.sleep(1)

        self.arm_motor.run_to_abs_pos(position_sp=0, speed_sp=self.MAX_SPEED)
        self.arm_motor.wait_while(ev3.Motor.STATE_RUNNING)
        time.sleep(1)

    def follow_line(self, color):
        """goes in a straight line until it reaches the given color or detects
        an object - additional feature of following a white line commented
        out due to the robot literally ripping the paper as it tried to
        navigate"""
        speed = 200
        print(color)
        if color == 'blue':
            color = self.color_sensor.COLOR_BLUE
        elif color == 'red':
            color = self.color_sensor.COLOR_RED
        elif color == 'green':
            color = self.color_sensor.COLOR_GREEN
        elif color == 'black':
            color = self.color_sensor.COLOR_BLACK
        elif color == 'yellow':
            color = self.color_sensor.COLOR_YELLOW
        self.drive(speed, speed)
        while self.color_sensor.color != color:  # and self.ir_sensor.proximity
            #  > 10:
            time.sleep(.01)
            # self.drive(200, 200)
            # time.sleep(.5)
            # while self.color_sensor.color == self.color_sensor.COLOR_WHITE:
            #     time.sleep(.01)
            #     if self.color_sensor.color == color:
            #         self.stop()
            #         break
            #     elif self.ir_sensor.proximity <= 10:
            #         self.stop()
            #         break
            # while self.color_sensor.color != self.color_sensor.COLOR_WHITE:
            #     self.turn_degrees(10, 100)
            #     if self.color_sensor.color == self.color_sensor.COLOR_WHITE:
            #         break
            #     elif self.color_sensor.color == color:
            #         break
            #     elif self.ir_sensor.proximity <= 10:
            #         break
            #     self.turn_degrees(-10, 100)
            #     if self.color_sensor.color == self.color_sensor.COLOR_WHITE:
            #         break
            #     elif self.color_sensor.color == color:
            #         break
            #     elif self.ir_sensor.proximity <= 10:
            #         break
            #     self.turn_degrees(-10, 100)
            #     if self.color_sensor.color == self.color_sensor.COLOR_WHITE:
            #         break
            #     elif self.color_sensor.color == color:
            #         break
            #     elif self.ir_sensor.proximity <= 10:
            #         break
            #     self.turn_degrees(10, 100)
            #     if self.color_sensor.color == self.color_sensor.COLOR_WHITE:
            #         break
            #     elif self.color_sensor.color == color:
            #         break
            #     elif self.ir_sensor.proximity <= 10:
            #         break
            #     self.turn_degrees(15, 100)
            #     if self.color_sensor.color == self.color_sensor.COLOR_WHITE:
            #         break
            #     elif self.color_sensor.color == color:
            #         break
            #     elif self.ir_sensor.proximity <= 10:
            #         break
            #     self.turn_degrees(-15, 100)
            #     if self.color_sensor.color == self.color_sensor.COLOR_WHITE:
            #         break
            #     elif self.color_sensor.color == color:
            #         break
            #     elif self.ir_sensor.proximity <= 10:
            #         break
            #     self.turn_degrees(-15, 100)
            #     if self.color_sensor.color == self.color_sensor.COLOR_WHITE:
            #         break
            #     elif self.color_sensor.color == color:
            #         break
            #     elif self.ir_sensor.proximity <= 10:
            #         break
            #     self.turn_degrees(15, 100)
            #     if self.color_sensor.color == self.color_sensor.COLOR_WHITE:
            #         break
            #     elif self.color_sensor.color == color:
            #         break
            #     elif self.ir_sensor.proximity <= 10:
            #         break
            # if self.color_sensor.color == color:
            #     break
            # elif self.ir_sensor.proximity <= 10:
            #     break
        self.stop()
        if self.ir_sensor.proximity < 10:
            return True
        else:
            return False
