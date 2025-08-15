# viewport_tracker.py
"""
Viewport tracking functions for creating a smooth "virtual camera".
"""

import cv2
import numpy as np


# This function calculates the region of interest (ROI) for the viewport tracker.
# It chooses a strategy for determining the main area of interest.
# strategy could be the largest motion box, a combination of nearby boxes, or a weighted average of all motion boxes.
# @param motion_boxes: List of motion detection bounding boxes
# @param frame_shape: Shape of the video frame (height, width)
# @return: Tuple (roi_center_x, roi_center_y, w, h) representing the region of interest center point and dimensions
def calculate_region_of_interest(motion_boxes, frame_shape):
    
    if not motion_boxes:
        # If no motion is detected, use the center of the frame
        height, width = frame_shape[:2]
        default_size = min(width, height) // 6
        return (width // 2, height // 2, default_size, default_size)
    
    # Strategy: weighted average of motion boxes, with larger boxes having more influence
    total_weight = 0
    weighted_x = 0
    weighted_y = 0
    total_width = 0
    total_height = 0
    
    for (x, y, w, h) in motion_boxes:
        # Calculate center of this motion box
        center_x = x + w // 2
        center_y = y + h // 2
        # Use area as weight (larger motion regions are more important)
        weight = w * h
        # Update weighted sums
        weighted_x += center_x * weight  # weighted_x is the sum of x coordinates weighted by area
        weighted_y += center_y * weight  # weighted_y is the sum of y coordinates weighted by area
        total_weight += weight
        # Accumulate widths and heights for averaging
        total_width += w
        total_height += h
    
    if total_weight > 0:
        # Calculate weighted average coordinates
        roi_center_x = int(weighted_x / total_weight)  # roi_center_x is the weighted average x coordinate
        roi_center_y = int(weighted_y / total_weight)  # roi_center_y is the weighted average y coordinate
        # Calculate average dimensions
        avg_width = int(total_width / len(motion_boxes))
        avg_height = int(total_height / len(motion_boxes))
        return (roi_center_x, roi_center_y, avg_width, avg_height)
    else:
        # Fallback to center of frame
        height, width = frame_shape[:2]
        default_size = min(width, height) // 6
        return (width // 2, height // 2, default_size, default_size)

def track_viewport(frames, motion_results, viewport_size, smoothing_factor=0.3):
    """
    Track viewport position across frames with smoothing.

    Args:
        frames: List of video frames
        motion_results: List of motion detection results for each frame
        viewport_size: Tuple (width, height) of the viewport
        smoothing_factor: Factor for smoothing viewport movement (0-1)
                          Lower values create smoother movement

    Returns:
        List of viewport positions for each frame as (x, y) center coordinates
    """
    # TODO: Implement viewport tracking with smoothing
    # 1. For each frame, determine the region of interest based on motion_results
    # 2. Apply smoothing to avoid jerky movements
    #    - Use previous viewport positions to smooth the movement
    #    - Consider implementing a simple exponential moving average
    #    - Or a more advanced approach like Kalman filtering
    # 3. Ensure the viewport stays within the frame boundaries
    # 4. Return the list of viewport positions for all frames

    # # Example starter code:
    # viewport_positions = []

    # # Initialize with center of first frame if available
    # if frames:
    #     height, width = frames[0].shape[:2]
    #     prev_x, prev_y = width // 2, height // 2
    # else:
    #     return []

    # Your implementation here
    if not frames:
        return []
    
    height, width = frames[0].shape[:2] 
    prev_x, prev_y = width // 2, height // 2  # start in center
    vp_w, vp_h = viewport_size
    viewport_positions = []

    for frame, motion_boxes in zip(frames, motion_results):
        # Get the region of interest for this frame
        cx, cy, _, _ = calculate_region_of_interest(motion_boxes, frame.shape)

        # Apply exponential smoothing
        smooth_x = int(smoothing_factor * cx + (1 - smoothing_factor) * prev_x)
        smooth_y = int(smoothing_factor * cy + (1 - smoothing_factor) * prev_y)

        # Keep viewport inside frame
        half_w = vp_w // 2
        half_h = vp_h // 2
        smooth_x = max(half_w, min(width - half_w, smooth_x))
        smooth_y = max(half_h, min(height - half_h, smooth_y))

        viewport_positions.append((smooth_x, smooth_y))

        prev_x, prev_y = smooth_x, smooth_y

    return viewport_positions
