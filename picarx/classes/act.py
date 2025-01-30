from picarx_improved import Picarx

class Controller:
    def __init__(self, scaling_factor=1.0):
        self.scaling_factor = scaling_factor
        self.picarx = Picarx()

    def control(self, offset):
        # Calculate the steering angle based on the offset and scaling factor
        steering_angle = self.scaling_factor * offset
        
        # Call the steering-servo method from picarx_improved.py
        self.picarx.set_dir_servo_angle(steering_angle)
        
        # Return the commanded steering angle
        return steering_angle
