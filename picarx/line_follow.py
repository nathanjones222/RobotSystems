import cv2
import numpy as np
from robot_hat import Servo
import time

class CameraSensor:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)  # Open default camera
        time.sleep(0.5)  # Allow camera to initialize

    def read_data(self):
        ret, frame = self.cap.read()
        if not ret:
            return 0  # No frame captured
        
        # Convert to HSV
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Define color range for line detection (Adjust as needed)
        lower_black = np.array([0, 0, 0])
        upper_black = np.array([180, 255, 50])

        # Create mask
        mask = cv2.inRange(hsv, lower_black, upper_black)

        # Find contours
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        if contours:
            largest_contour = max(contours, key=cv2.contourArea)
            M = cv2.moments(largest_contour)
            
            if M["m00"] != 0:
                line_x = int(M["m10"] / M["m00"])  # Centroid X-coordinate
                frame_center = frame.shape[1] // 2  # Assuming 640x480 resolution
                error = (line_x - frame_center) / frame_center  # Normalize error (-1 to 1)
            else:
                error = 0
        else:
            error = 0  # No line detected
        
        return error
    
    def release(self):
        self.cap.release()
        cv2.destroyAllWindows()

class Interpreter:
    def __init__(self, k_p=1.0, k_i=0.0, k_d=0.0):
        self.k_p = k_p
        self.k_i = k_i
        self.k_d = k_d
        self.last_error = 0
        self.sum_error = 0

    def interpret_camera_data(self, error):
        # Calculate PID values
        p_term = self.k_p * error
        i_term = self.k_i * self.sum_error
        d_term = self.k_d * (error - self.last_error)
        
        # Compute turn proportion
        turn_proportion = p_term + i_term + d_term
        turn_proportion = max(-1, min(1, turn_proportion))  # Clamp to [-1, 1]
        
        # Update errors
        self.sum_error += error
        self.last_error = error
        
        return turn_proportion

class Controller:
    def __init__(self, angle_max=30):
        self.angle_max = angle_max
        self.turn_servo = Servo("P2")

    def set_turn_proportion(self, turn_proportion):
        turning_angle = float(self.angle_max * turn_proportion)
        self.turn_servo.angle(turning_angle)

# Example usage
if __name__ == "__main__":
    sensor = CameraSensor()
    interpreter = Interpreter(k_p=0.5, k_i=0.01, k_d=0.1)
    controller = Controller(angle_max=30)
    
    try:
        while True:
            error = sensor.read_data()
            if error is not None:
                turn_proportion = interpreter.interpret_camera_data(error)
                controller.set_turn_proportion(turn_proportion)
                print(f"Turn Proportion: {turn_proportion}, Steering Angle: {turn_proportion * 30}")
            time.sleep(0.05)
    finally:
        sensor.release()
        print("Camera released and exiting.")
