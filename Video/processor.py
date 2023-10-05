import os
import cv2
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip


directory_path = 'videos/'
save_path = 'videos/processed'

files_and_directories = os.listdir(directory_path)
files = [file for file in files_and_directories if os.path.isfile(os.path.join(directory_path, file))]
for file in files:
    fp = os.path.join(directory_path, file)

    video_capture = cv2.VideoCapture(fp)
    fps = int(video_capture.get(cv2.CAP_PROP_FPS))

    # Initialize background subtractor (change this to suit your needs)
    bg_subtractor = cv2.createBackgroundSubtractorMOG2(varThreshold=993.4)

    # Variables for recording the start and end frames of the action
    start_frame = None
    end_frame = None

    # Loop through the video frames
    crop_left_percentage = 20  # Crop 20% from the left
    crop_right_percentage = 20  # Crop 20% from the right

    # Calculate the cropping boundaries
    frame_width = int(video_capture.get(3))
    crop_left = int(frame_width * (crop_left_percentage / 100))
    crop_right = frame_width - int(frame_width * (crop_right_percentage / 100))

    frame_number = 0
    while True:
        ret, frame = video_capture.read()
        if not ret:
            break
        
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Apply background subtraction to detect motion
        frame = frame[:, crop_left:crop_right]

        fg_mask = bg_subtractor.apply(frame)

        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        fg_mask = cv2.erode(fg_mask, kernel, iterations=1)
        fg_mask = cv2.dilate(fg_mask, kernel, iterations=1)

        # Threshold the mask to get binary motion mask
        thresh = 250  # You may need to adjust this threshold
        motion_mask = cv2.threshold(fg_mask, thresh, 255, cv2.THRESH_BINARY)[1]
        
        # Check if there is motion in the frame
        if motion_mask.any():
            if start_frame is None:
                start_frame = frame_number
            end_frame = frame_number

        frame_number += 1

        cv2.waitKey(0) 

    # Release video capture
    video_capture.release()

    # Start and end frame (in seconds)
    start_time = start_frame/fps
    end_time = end_frame/fps

    # Output video file path
    output_file = os.path.join(save_path, file)

    # Crop and save the video
    ffmpeg_extract_subclip(fp, start_time, end_time, targetname=output_file)
