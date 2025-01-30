import time
import numpy as np
import os
try:
    from robot_hat import Pin, ADC, PWM, Servo, fileDB
    from robot_hat import Grayscale_Module, Ultrasonic, utils
except ImportError:
    import sys
    sys.path.append(os.path.abspath(os.path.join(
    os.path.dirname(__file__), "..")))
    from sim_robot_hat import Pin, ADC, PWM, Servo, fileDB
    from sim_robot_hat import Grayscale_Module, Ultrasonic, utils

class Controller():
    def __init__(self, max_turn_angle=30):
        self.max_turn_angle=max_turn_angle
        self.turn_servo = Servo("P2")

    def set_turn_proportion(self, turn_proportion):
        turn_angle = float(self.max_turn_angle*turn_proportion)
        self.turn_servo.angle(turn_angle)