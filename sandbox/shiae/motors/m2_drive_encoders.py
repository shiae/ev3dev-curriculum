#!/usr/bin/env python3
"""
This module lets you practice using the encoder to determine distances while blocking code execution until complete.

You will now use a run_to_rel_pos command to implement the action drive inches action.

Authors: David Fisher and Allison, Ryan, and Stephen.
"""  # DONE: 1. PUT YOUR NAME IN THE ABOVE LINE.

# DONE: 2. Copy the contents of your m1_drive_timed.py and paste that text
# into this file below these comments.
#   If your program says and prints anything at the start change it to print and say "Drive using encoders"

# DONE: 3. Add a beep after the drive motors stop (see code below).  Test your
# code to hear the beep AFTER movement.
#   ev3.Sound.beep().wait()

# TODO: 4. Instead of using the run_forever, time.sleep, stop pattern switch to using the run_to_rel_pos command.
#   You will need to determine the position_sp value to pass into the run_to_rel_pos command as a named argument.
#   Assume the diameter of the wheel is 1.3" (close enough).  A 1.3" diameter wheel results in approximately a 4"
#     circumference, so 360 degrees = 4 inches of travel.
#   So you need to move through roughly 90 degrees for every inch of travel. That value is very handy!
#
#       degrees_per_inch = 90
#       motor_turns_needed_in_degrees = inches_target * degrees_per_inch
#
#   Delete your time.sleep and .stop commands as well as your speed equations to get time (we no longer care about time)
#     and convert your run_forever method to use a run_to_rel_pos method with appropriate arguments.
#   Your arguments to the run_to_rel_pos method should include the named arguments (notice time is not needed):
#        -- position_sp
#        -- speed_sp
#        -- stop_action

# TODO: 5. Make sure the beep happens AFTER the motors stop.  Use the wait_while command to block code execution.

# TODO: 6. Formally test your work. When you think you have the problem complete run these tests:
#   200 dps 24 inches (make sure it drives within 2 inches of the target distance)
#   400 dps 24 inches (make sure it drives within 2 inches of the target distance)
#   800 dps 24 inches (make sure it drives within 2 inches of the target distance)
#   400 dps 12 inches (make sure it drives within 1 inches of the target distance)
#   400 dps 36 inches (make sure it drives within 3 inches of the target distance)
#   400 dps -36 inches (make sure it drives within 3 inches of the target distance)
# Add more tests as you see fit.  Ideally you should be +/- 10% of the target goal this time.

# TODO: 7. Call over a TA or instructor to sign your team's checkoff sheet and do a code review.
#
# Observations you should make, run_to_rel_pos is easier to use since it uses encoders that are independent of speed.

import ev3dev.ev3 as ev3
import time
import math

def main():

    print("--------------------------------------------")
    print("  Drive using Encoders")
    print("--------------------------------------------")
    ev3.Sound.speak("Drive Using Encoders").wait()

    # Connect two large motors on output ports B and C
    left_motor = ev3.LargeMotor(ev3.OUTPUT_B)
    right_motor = ev3.LargeMotor(ev3.OUTPUT_C)

    # Check that the motors are actually connected
    assert left_motor.connected
    assert right_motor.connected

    time_s = 1  # Any value other than 0.
    while time_s != 0:
        # v = int(input("Enter a speed (0 to 900 dps): "))
        # x = int(input("Distance to travel (inches): "))
        y = 90 * int(input("Distance to travel (inches): "))
        s = int(input("Enter a speed (0 to 900 dps): "))

        # time_s = 1 / ((9.2032635351028/(1 + 8.5531895233376 * math.exp(
        #     -.0054156306930 * v))) / x)

        # left_motor.run_forever(speed_sp=v)
        # right_motor.run_forever(speed_sp=v)
        # time.sleep(time_s)
        # right_motor.stop()
        # left_motor.stop()

        left_motor.run_to_rel_pos(position_sp=y, speed_sp=s)
        right_motor.run_to_rel_pos(position_sp=y, speed_sp=s)\
        right_motor.wait_while(right_motor.STATE_RUNNING)
        ev3.Sound.beep().wait()


    print("Goodbye!")
    ev3.Sound.speak("Goodbye").wait()


# ----------------------------------------------------------------------
# Calls  main  to start the ball rolling.
# ----------------------------------------------------------------------
main()
