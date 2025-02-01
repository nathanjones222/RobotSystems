import numpy as np

class Interpreter:
    def __init__(self, line_threshold=35, sensitivity=1.0, line_dark=True):
        # initialize the interpreter with given parameters
        self.sensitivity = sensitivity
        self.line_dark = line_dark
        self.line_threshold = line_threshold
        self.last_sensor_to_detect_line = 1
        self.last_error = 0
        self.sum_error = 0


    def interpret_sensor_reading_PID(self, sensor_reading, k_p=1.0, k_i=0.0, k_d=0.0):
        # interpret sensor reading using a PID controller
        if self._is_difference_insignificant(sensor_reading):
            return 1 - self.last_sensor_to_detect_line

        # average readings for the left and right sensors
        left_avg = np.mean(sensor_reading[:2])
        right_avg = np.mean(sensor_reading[1:3])
        error = left_avg - right_avg

        # calculate the PID value
        pid = k_p * error + k_i * (self.sum_error + error) + k_d * (error - self.last_error)
        pid *= 0.05

        # calculate turn proportion using a sigmoid function
        turn_proportion = 2 / (1 + np.exp(-pid)) - 1
        print(f"{left_avg} - {right_avg} = {error}")
        print(f"{pid} = {turn_proportion}")

        self.sum_error += error
        self.last_error = error

        return turn_proportion

    def _is_difference_insignificant(self, sensor_reading):
        if not self.line_dark:
            sensor_reading = -sensor_reading

        # index of sensor with greatest reading
        line_index = np.argmax(sensor_reading)
        ground_indices = [i for i in range(3) if i != line_index]

        # find line reading and average ground reading
        line_reading = sensor_reading[line_index]
        avg_ground_reading = np.mean(sensor_reading[ground_indices])
        ground_line_difference = np.abs(line_reading - avg_ground_reading)

        # check if within threshold
        if ground_line_difference <= (self.line_threshold / self.sensitivity):
            return True
        else:
            print(ground_line_difference)
            self.last_sensor_to_detect_line = line_index
            return False
