# frame_processor.py
"""
Frame processing functions for the motion detection project.
"""

import cv2
import numpy as np

# @param video_path: Path to the video file
# @param target_fps: Target frames per second to extract
# @param resize_dim: Dimensions to resize frames to (width, height)
# return: List of extracted frames
def process_video(video_path, target_fps=5, resize_dim=(1280, 720)):

    frames = []

    # Open the video file
    cap = cv2.VideoCapture(video_path)

    # Get video properties
    original_fps = cap.get(cv2.CAP_PROP_FPS)                # Get the original frames per second
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))   # Get the total number of frames

    print(f"Original video FPS: {original_fps}")
    print(f"Total frames in video: {total_frames}")
    print(f"Target FPS: {target_fps}")

    # Calculate frame skip interval
    frame_skip = int(original_fps / target_fps)
    print(f"Extracting every {frame_skip} frames")

    
    frame_count = 0                  # Counter to keep track of current frame number
    extracted_count = 0              # Counter to keep track of extracted frames

    # Loop through each frame of the video
    while True:
        # Read the next frame
        ret, frame = cap.read()
        if not ret:
            break

        # Extract frame at the target interval
        if frame_count % frame_skip == 0:
            # Resize the frame to standard dimensions
            resized_frame = cv2.resize(frame, resize_dim)
            frames.append(resized_frame)
            extracted_count += 1

        frame_count += 1
    
    cap.release()  # Release the video capture object

    print(f"Successfully extracted {extracted_count} frames")

    return frames

