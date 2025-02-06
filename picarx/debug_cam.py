import cv2

cap = cv2.VideoCapture(0)  # Try 1 instead of 0 if it doesn't work

if not cap.isOpened():
    print("[ERROR] Camera not detected!")
else:
    print("[SUCCESS] Camera is working.")

cap.release()