import time
import numpy as np
import os
try:
    from robot_hat import Pin, ADC, PWM, Servo, fileDB
    from robot_hat import Grayscale_Module, Ultrasonic, utils
    on_the_robot = True
except ImportError:
    import sys
    sys.path.append(os.path.abspath(os.path.join(
    os.path.dirname(__file__), "..")))
    from sim_robot_hat import Pin, ADC, PWM, Servo, fileDB
    from sim_robot_hat import Grayscale_Module, Ultrasonic, utils
    on_the_robot = False

class Controller():
    def __init__(self, angle_max=30):
        self.angle_max = angle_max
        self.turn_servo = Servo("P2")

    def set_turn_proportion(self, turn_proportion):
        turning_angle = float(self.angle_max*turn_proportion)
        self.turn_servo.angle(turning_angle)