import cv2
import numpy as np
import time
from picarx import Picarx
from picamera2 import Picamera2, Preview

# Enable debugging mode (Set to False for normal operation)
DEBUG_MODE = True

class CameraSensor:
    def __init__(self):
        # Initialize Picamera2
        self.camera = Picamera2()
        self.camera.configure(self.camera.create_still_configuration())
        self.camera.start()
        time.sleep(1)  # Allow camera to initialize

    def read_data(self):
        # Capture a frame using Picamera2
        frame = self.camera.capture_array("main")
        frame = cv2.resize(frame, (320, 240))
        
        # Convert to HSV color space
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Define HSV range for line detection
        lower_black = np.array([0, 0, 0])   # Adjust if needed
        upper_black = np.array([180, 255, 120])  

        # Create mask
        mask = cv2.inRange(hsv, lower_black, upper_black)

        # Find contours
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if DEBUG_MODE:
            # Show Raw Camera Feed
            cv2.imshow("Raw Camera Feed", frame)
            
            # Show Line Mask
            cv2.imshow("Line Mask", mask)

            # Print Contour Count
            print(f"[DEBUG] Number of contours detected: {len(contours)}")

            # If debugging, allow user to click and check HSV values
            def pick_color(event, x, y, flags, param):
                if event == cv2.EVENT_LBUTTONDOWN:
                    pixel = hsv[y, x]
                    print(f"[DEBUG] HSV Value at ({x}, {y}): {pixel}")
            
            cv2.setMouseCallback("Raw Camera Feed", pick_color)

            cv2.waitKey(1)

        if contours:
            largest_contour = max(contours, key=cv2.contourArea)
            M = cv2.moments(largest_contour)
            
            if M["m00"] != 0:
                line_x = int(M["m10"] / M["m00"])  # Get X position of centroid
                frame_center = frame.shape[1] // 2  # Assuming 640x480 resolution
                error = (line_x - frame_center) / frame_center  # Normalize error (-1 to 1)

                # Draw detected line
                cv2.drawContours(frame, [largest_contour], -1, (0, 255, 0), 2)
                cv2.circle(frame, (line_x, frame.shape[0] // 2), 5, (0, 0, 255), -1)
                if DEBUG_MODE:
                    cv2.imshow("Contours", frame)

            else:
                error = 0
        else:
            print("[WARNING] No line detected")
            error = 0  # No line detected

        return error
    
    def release(self):
        self.camera.stop()
        cv2.destroyAllWindows()

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
        
        turn_proportion = p_term + i_term + d_term
        turn_proportion = max(-1, min(1, turn_proportion))  # Clamp to [-1, 1]
        
        # Debug: Print PID components
        if DEBUG_MODE:
            print(f"[DEBUG] P: {p_term:.2f}, I: {i_term:.2f}, D: {d_term:.2f}, Turn Proportion: {turn_proportion:.2f}")

        # Update errors
        self.sum_error += error
        self.sum_error = max(-1, min(1, self.sum_error))
        self.last_error = error
        
        return turn_proportion

# Main execution loop
if __name__ == "__main__":
    px = Picarx()
    sensor = CameraSensor()
    interpreter = Interpreter(k_p=0.5, k_i=0.01, k_d=0.1)

    input("Press Enter to start line following...")  # Wait for user input

    try:
        px.forward(25)  # Set constant forward speed
        px.set_cam_tilt_angle(-30)

        while True:
            error = sensor.read_data()
            turn_proportion = interpreter.interpret_camera_data(error)
            turn_angle = turn_proportion * 30  # Scale to servo range
            
            px.set_dir_servo_angle(turn_angle)
            
            # Debug: Print error and steering angle
            if DEBUG_MODE:
                print(f"[INFO] Error: {error:.2f}, Turn Angle: {turn_angle:.2f}")
            
            time.sleep(0.1)
    
    except KeyboardInterrupt:
        px.stop()
        sensor.release()
        print("[INFO] Stopped and exiting.")




