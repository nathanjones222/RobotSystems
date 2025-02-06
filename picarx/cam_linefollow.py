import time
from picarx import Picarx
from vilib import Vilib

class CameraSensor:
    def __init__(self):
        # Start camera and initialize Vilib
        Vilib.camera_start()
        Vilib.display()  # To show camera feed
        Vilib.line_following_switch(True)  # Enable line following mode
        time.sleep(0.5)  # Allow camera to initialize

    def read_data(self):
        # Detect the line using Vilib (line_x is the detected line position)
        line_x = Vilib.detect_obj_parameter.get('line_x', -1)
        
        # Assume frame center is at 320 (for 640x480 resolution)
        frame_center = 320

        # If line is detected, calculate error (normalized to [-1, 1])
        if line_x != -1:
            error = (line_x - frame_center) / frame_center  # Normalize error
        else:
            error = 0  # No line detected
        
        return error

    def release(self):
        # Stop line following and release the camera
        Vilib.line_following_switch(False)
        Vilib.camera_close()

class Interpreter:
    def __init__(self, k_p=0.5, k_i=0.01, k_d=0.1):
        self.k_p = k_p
        self.k_i = k_i
        self.k_d = k_d
        self.last_error = 0
        self.sum_error = 0

    def interpret_camera_data(self, error):
        # PID Control
        p_term = self.k_p * error
        i_term = self.k_i * self.sum_error
        d_term = self.k_d * (error - self.last_error)
        
        # Calculate the turn proportion
        turn_proportion = p_term + i_term + d_term
        turn_proportion = max(-1, min(1, turn_proportion))  # Clamp to [-1, 1]
        
        # Update errors
        self.sum_error += error
        self.last_error = error
        
        return turn_proportion

class Controller:
    def __init__(self, angle_max=30):
        self.angle_max = angle_max
        self.turn_servo = Picarx().get_servo("P2")  # Get the steering servo

    def set_turn_proportion(self, turn_proportion):
        # Convert turn proportion to steering angle
        turning_angle = float(self.angle_max * turn_proportion)
        self.turn_servo.angle(turning_angle)

# Main execution loop
if __name__ == "__main__":
    px = Picarx()  # Initialize the robot
    sensor = CameraSensor()  # Initialize the camera sensor
    interpreter = Interpreter(k_p=0.5, k_i=0.01, k_d=0.1)  # Initialize the interpreter
    controller = Controller(angle_max=30)  # Initialize the controller

    try:
        px.forward(30)  # Set constant forward speed

        while True:
            # Get error from the sensor (how much the line deviates from the center)
            error = sensor.read_data()

            # Get turn proportion using PID controller
            turn_proportion = interpreter.interpret_camera_data(error)

            # Set the steering angle based on the turn proportion
            controller.set_turn_proportion(turn_proportion)

            print(f"Error: {error}, Turn Proportion: {turn_proportion}")

            time.sleep(0.05)
    
    except KeyboardInterrupt:
        # Stop robot and release resources on exit
        px.stop()
        sensor.release()
        print("Exiting line following.")


