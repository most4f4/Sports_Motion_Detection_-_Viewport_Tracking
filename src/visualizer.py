# visualizer.py
"""
Visualization functions for displaying motion detection and viewport tracking results.
"""

import os
import cv2
import numpy as np


def visualize_results(frames, motion_results, viewport_positions, viewport_size, output_dir):
    """
    Create visualization of motion detection and viewport tracking results.

    Args:
        frames: List of video frames
        motion_results: List of motion detection results for each frame
        viewport_positions: List of viewport center positions for each frame
        viewport_size: Tuple (width, height) of the viewport
        output_dir: Directory to save visualization results
    """
    # Create output directory for frames
    frames_dir = os.path.join(output_dir, "frames")
    os.makedirs(frames_dir, exist_ok=True)

    viewport_dir = os.path.join(output_dir, "viewport")
    os.makedirs(viewport_dir, exist_ok=True)

    # Get dimensions for the output video
    height, width = frames[0].shape[:2]

    # Create video writers
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    video_path = os.path.join(output_dir, "motion_detection.mp4")
    video_writer = cv2.VideoWriter(video_path, fourcc, 5, (width, height))

    viewport_video_path = os.path.join(output_dir, "viewport_tracking.mp4")
    vp_width, vp_height = viewport_size
    viewport_writer = cv2.VideoWriter(
        viewport_video_path, fourcc, 5, (vp_width, vp_height)
    )

    # TODO: Implement visualization
    
    # 1. Process each frame
    #    a. Create a copy of the frame for visualization
    #    b. Draw bounding boxes around motion regions
    #       (hint: cv2.rectangle with green color (0, 255, 0))
    #    c. Draw the viewport rectangle
    #       (hint: cv2.rectangle with blue color (255, 0, 0))
    #    d. Extract the viewport content (the area inside the viewport)
    #    e. Add frame number to the visualization (hint: cv2.putText)
    #    f. Save visualization frames and viewport frames as images
    #    g. Write frames to both video writers
    # 2. Release the video writers when done

    # Process each frame
    # Loop over frame indices
    for i in range(len(frames)):
        # Get current frame, motion boxes, and viewport position
        frame = frames[i]
        motion_boxes = motion_results[i]
        viewport_pos = viewport_positions[i]

        # Make a copy of the frame
        vis_frame = frame.copy()

        # Draw green boxes for motion regions
        # Each box is (x, y, w, h)
        for box in motion_boxes:
            x, y, w, h = box
            # Draw rectangle: top-left (x,y), bottom-right (x+w,y+h), green (0,255,0), thickness 2
            cv2.rectangle(vis_frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Draw blue viewport rectangle
        # Viewport_pos is (x,y) center, so calculate corners
        vp_x, vp_y = viewport_pos
        vp_half_w = vp_width // 2
        vp_half_h = vp_height // 2
        # Top-left is center minus half size, bottom-right is plus
        top_left = (vp_x - vp_half_w, vp_y - vp_half_h)
        bottom_right = (vp_x + vp_half_w, vp_y + vp_half_h)
        # Draw blue rectangle (255,0,0), thickness 2
        cv2.rectangle(vis_frame, top_left, bottom_right, (255, 0, 0), 2)

        # Add frame number text
        # Put at top-left (10,30), white (255,255,255), font scale 1
        cv2.putText(vis_frame, f"Frame: {i + 1}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        # Extract viewport content
        # Ensure crop stays within frame bounds
        start_x = max(0, vp_x - vp_half_w)
        end_x = min(width, vp_x + vp_half_w)
        start_y = max(0, vp_y - vp_half_h)
        end_y = min(height, vp_y + vp_half_h)
        # Slice frame to get viewport area
        viewport_frame = frame[start_y:end_y, start_x:end_x]

        # Resize viewport frame to exact viewport size
        viewport_frame = cv2.resize(viewport_frame, (vp_width, vp_height))

        # Save visualization frame and viewport frame as images
        # Use 4-digit numbering (e.g., frame_0001.png) for sorting
        frame_filename = os.path.join(frames_dir, f"frame_{i:04d}.png")
        viewport_filename = os.path.join(viewport_dir, f"viewport_{i:04d}.png")
        cv2.imwrite(frame_filename, vis_frame)
        cv2.imwrite(viewport_filename, viewport_frame)

        # Write frames to video files
        video_writer.write(vis_frame)
        viewport_writer.write(viewport_frame)

    # Release video writers to finalize videos
    video_writer.release()
    viewport_writer.release()

    print(f"Visualization saved to {video_path}")
    print(f"Viewport video saved to {viewport_video_path}")
    print(f"Individual frames saved to {frames_dir} and {viewport_dir}")