import cv2
import time 
from pyzbar.pyzbar import decode
import numpy as np

def try_camera_indices():
    """Try different camera indices to find one that works"""
    for i in range(3): 
        print(f"Attempting to open camera at index {i}")
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            ret, frame = cap.read()
            if ret:
                print(f"Successfully opened camera at index {i}")
                return cap
            cap.release()
    
    for i in range(3):
        print(f"Attempting to open camera at index {i} with DirectShow")
        cap = cv2.VideoCapture(i, cv2.CAP_DSHOW)  
        if cap.isOpened():
            ret, frame = cap.read()
            if ret:
                print(f"Successfully opened camera at index {i} with DirectShow")
                return cap
            cap.release()
    
    return None

# Try to capture webcam with multiple methods
cap = try_camera_indices()

# Check if the camera opened successfully
if cap is None:
    print("Error: Could not open any camera. Please check if the camera is connected and not in use by another application.")
    exit()

# Give the camera time to initialize
time.sleep(2)

try:
    while True:
        # Read a frame from the camera
        success, frame = cap.read()
        
        # Check if frame was successfully read
        if not success:
            print("Error: Failed to read frame from camera. Retrying...")
            # Give the camera a moment to recover
            time.sleep(0.5)
            continue
            
        # flip the image like mirror image 
        frame = cv2.flip(frame, 1)
        
        # detect the barcode 
        detectedBarcode = decode(frame)
        
        # if barcode detected 
        if detectedBarcode:
            # codes in barcode 
            for barcode in detectedBarcode:
                # if barcode is not blank 
                if barcode.data != "":
                    # Convert bytes to string for display
                    barcode_data = barcode.data.decode('utf-8')
                    # Draw a rectangle around the barcode
                    points = barcode.polygon
                    if points:
                        pts = [(int(p.x), int(p.y)) for p in points]
                        cv2.polylines(frame, [np.array(pts)], True, (0, 255, 0), 2)
                    
                    cv2.putText(frame, barcode_data, (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 255), 2)
                    print(f"Detected barcode: {barcode_data}")
                    # cv2.imwrite(f"detected_code_{barcode_data}.png", frame)

        # Display the frame
        cv2.imshow('Barcode Scanner', frame)
        
        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) == ord('q'):
            break

except KeyboardInterrupt:
    print("Program interrupted by user")
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    # Release the camera and close all windows
    print("Cleaning up resources...")
    if cap is not None:
        cap.release()
    cv2.destroyAllWindows()