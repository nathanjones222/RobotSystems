import time
import numpy as np

try:
    from robot_hat import Pin, ADC, PWM, Servo, fileDB
    from robot_hat import Grayscale_Module, Ultrasonic
    from robot_hat.utils import reset_mcu, run_command
    on_the_robot = True
    reset_mcu()
    time.sleep(0.2)

except ImportError:
    from sim_robot_hat import Pin, ADC, PWM, Servo, fileDB
    from sim_robot_hat import Grayscale_Module, Ultrasonic
    on_the_robot = False

class Sensor:
    def __init__(self):
        # initialize the ADC channels
        self.adc_channels = [ADC(i) for i in range(3)]

        self.current_index = 0
        self.sample_count = 3
        self.sensor_count = 3
        self.grayscale_values = np.zeros((self.sample_count, self.sensor_count))

        for sample in range(self.sample_count):
            for sensor in range(self.sensor_count):
                self.grayscale_values[sample, sensor] = self.adc_channels[sensor].read()

    def read_data(self):
        # read grayscale values from sensors
        for sensor in range(self.sensor_count):
            self.grayscale_values[self.current_index, sensor] = self.adc_channels[sensor].read()

        self.current_index = (self.current_index + 1) % self.sample_count

        averaged_data = np.mean(self.grayscale_values, axis=0)
        print("data:", averaged_data)
        # return the averaged grayscale values
        return averaged_data
        