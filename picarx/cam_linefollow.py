import cv2
import numpy as np
from robot_hat import Servo

class CameraSensor:
    def __init__(self, camera_index=0, frame_width=320, frame_height=240):
        self.cap = cv2.VideoCapture(camera_index)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, frame_width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, frame_height)

    def read_data(self):
        ret, frame = self.cap.read()
        if not ret:
            return None
        
        # Convert to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Apply Gaussian blur
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        
        # Edge detection
        edges = cv2.Canny(blurred, 50, 150)
        
        # Detect the line using Hough Transform
        lines = cv2.HoughLinesP(edges, 1, np.pi/180, 50, minLineLength=50, maxLineGap=10)
        
        if lines is not None:
            line_positions = [line[0][0] for line in lines]  # Extract x-coordinates of lines
            avg_position = np.mean(line_positions)  # Compute average x position
            frame_center = frame.shape[1] / 2  # Get frame center
            error = (avg_position - frame_center) / frame_center  # Normalize error (-1 to 1)
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
    
    while True:
        error = sensor.read_data()
        if error is not None:
            turn_proportion = interpreter.interpret_camera_data(error)
            controller.set_turn_proportion(turn_proportion)
            print(f"Turn Proportion: {turn_proportion}, Steering Angle: {turn_proportion * 30}")
