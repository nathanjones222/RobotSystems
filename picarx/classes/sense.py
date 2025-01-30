import os
import sys
from sim_robot_hat.modules import Grayscale_Module
from sim_robot_hat.pin import Pin
from sim_robot_hat.pwm import PWM
from sim_robot_hat.adc import ADC
from sim_robot_hat.i2c import I2C
import time
from sim_robot_hat.basic import _Basic_class
from typing import Union, List, Tuple, Optional
sys.path.append(os.path.abspath(os.path.join(
os.path.dirname(__file__), "..")))

from picarx import Picarx
px = Picarx()
grayscale = Grayscale_Module()

class Sense():
    def __init__(self, pin0: ADC, pin1: ADC, pin2: ADC, reference: int = None):
        self.pins = (pin0, pin1, pin2)
    def grayscale_data(self, channel: int = None) -> list:
        if channel == None:
            return [self.pins[i].read() for i in range(3)]
        else:
            return self.pins[channel].read()
# def get_grayscale_data(self):
    #     grayscale_data = list.copy(grayscale.read())
    #     return grayscale_data
    
