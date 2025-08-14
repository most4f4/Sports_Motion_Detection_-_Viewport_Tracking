# motion_detector.py
"""
Motion detection functions for the sports video analysis project.
"""

import cv2
import numpy as np

# @param frames: List of video frames extracted from the original video file
# @param frame_idx: Index of the current frame in the list to compare with the previous frame
# @param threshold: Pixel intensity difference threshold to decide if a change is considered motion
# @param min_area: Minimum contour area in pixels; anything smaller is ignored as noise
# return: List of bounding boxes for detected motion regions
def detect_motion(frames, frame_idx, threshold=25, min_area=100):

    # We need at least 2 frames to detect motion
    if frame_idx < 1 or frame_idx >= len(frames):
        return []

    # Get current and previous frame
    current_frame = frames[frame_idx]
    prev_frame = frames[frame_idx - 1]

    motion_boxes = []  # List to hold bounding boxes of detected motion (x, y, width, height)

    try:
        # 1. Convert frames to grayscale to reduce complexity
        # color is not needed for detecting motion; only brightness changes matter
        gray_current = cv2.cvtColor(current_frame, cv2.COLOR_BGR2GRAY)
        gray_prev = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)

        # 2. Apply Gaussian blur to reduce noise (random pixel changes)
        # (21, 21) is the size of the Gaussian kernel
        blurred_current = cv2.GaussianBlur(gray_current, (21, 21), 0)
        blurred_prev = cv2.GaussianBlur(gray_prev, (21, 21), 0)

        # 3. Calculate absolute difference in brightness between the two frames
        # frame_diff is now the new produced frame
        frame_diff = cv2.absdiff(blurred_prev, blurred_current)

        # 4. Apply threshold to highlight differences
        # It turns the difference image into a binary image
        # Pixels with a value above the threshold become white (255), and below become black (0)
        _, thresh = cv2.threshold(frame_diff, threshold, 255, cv2.THRESH_BINARY)

        # 5. Dilate the thresholded image to fill in holes
        # This helps to connect nearby white regions and make contours easier to find
        # (5, 5) is the size of the structuring element used for dilation
        # iterations=2 expands motion areas more than once.
        kernel = np.ones((5, 5), np.uint8)
        dilated = cv2.dilate(thresh, kernel, iterations=2)

        # 6. Finds the contours of connected white areas in the dilated image
        # contours are the boundaries of these white regions
        # cv2.RETR_EXTERNAL retrieves only the extreme outer contours (ignores nested ones)
        # cv2.CHAIN_APPROX_SIMPLE compresses contour points (leaves only their end points) to save memory 
        contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # 7. Filter contours by area and extract bounding boxes
        for contour in contours:

            area = cv2.contourArea(contour)  # Calculate contour area (number of pixels)

            # Determine if the contour is significant enough to be considered motion
            if area > min_area:
                # Get bounding rectangle around the contour
                x, y, w, h = cv2.boundingRect(contour)

                # Append the bounding box to the list of motion boxes
                motion_boxes.append((x, y, w, h))
                    
        # Sort boxes by area (width × height) in descending order to prioritize significant motion
        # lambda b: b[2] * b[3] means: Take a box b, Multiply b[2] (width) * b[3] (height)
        motion_boxes = sorted(motion_boxes, key=lambda b: b[2] * b[3], reverse=True)

    except Exception as e:
        # Log the error if anything goes wrong
        print(f"Error in motion detection for frame {frame_idx}: {e}")
        return []

    # If no errors occurred, return the list of motion boxes
    return motion_boxes