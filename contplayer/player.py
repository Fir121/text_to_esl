import cv2
import os
from moviepy.editor import VideoFileClip, concatenate_videoclips
import mediapipe as mp
import numpy as np
import uuid

video_dir = 'videos/processed/'

def play_files_with_mediapipe(video_files):
    mp_drawing = mp.solutions.drawing_utils
    mp_holistic = mp.solutions.hands
    frame_width = frame_height = size = result = None
    with mp_holistic.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
        for video_file in video_files:
            video_path = os.path.join(video_dir, video_file)

            # Create a VideoCapture object
            cap = cv2.VideoCapture(video_path)
            
            if not cap.isOpened():
                print(f"Could not open video file: {video_path}")
                continue
            if size is None:
                frame_width = int(cap.get(3)) 
                frame_height = int(cap.get(4)) 
                
                size = (frame_width, frame_height) 
                result = cv2.VideoWriter('output.avi',  
                         cv2.VideoWriter_fourcc(*'MJPG'), 
                         10, size) 

            # Play the video
            while True:
                ret, frame = cap.read()
                if not ret:
                    break

                # Recolor Feed
                image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                # Make Detections
                results = holistic.process(image)
                # print(results.face_landmarks)
                
                # face_landmarks, pose_landmarks, left_hand_landmarks, right_hand_landmarks
                
                # Recolor image back to BGR for rendering
                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
                image = np.zeros((image.shape[0], image.shape[1], 3), dtype = "uint8")
                
                # 1. Draw face landmarks
                # mp_drawing.draw_landmarks(image, results.face_landmarks, mp_holistic.FACEMESH_CONTOURS, 
                #                         mp_drawing.DrawingSpec(color=(80,110,10), thickness=1, circle_radius=1),
                #                         mp_drawing.DrawingSpec(color=(80,256,121), thickness=1, circle_radius=1)
                #                         )
                
                # 2. Right hand
                # mp_drawing.draw_landmarks(image, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS, 
                #                         mp_drawing.DrawingSpec(color=(80,22,10), thickness=1, circle_radius=3),
                #                         mp_drawing.DrawingSpec(color=(80,44,121), thickness=1, circle_radius=2)
                #                         )

                # # 3. Left Hand
                # mp_drawing.draw_landmarks(image, results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS, 
                #                         mp_drawing.DrawingSpec(color=(121,22,76), thickness=1, circle_radius=3),
                #                         mp_drawing.DrawingSpec(color=(121,44,250), thickness=1, circle_radius=2)
                #                         )
            
                if results.multi_hand_landmarks:
                    for hand_landmarks in results.multi_hand_landmarks:
                        mp_drawing.draw_landmarks(image, hand_landmarks , mp_holistic.HAND_CONNECTIONS, 
                                            mp_drawing.DrawingSpec(color=(121,22,76), thickness=1, circle_radius=3),
                                            mp_drawing.DrawingSpec(color=(121,44,250), thickness=1, circle_radius=2)
                                            )

                # 4. Pose Detections
                # mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS, 
                #                         mp_drawing.DrawingSpec(color=(245,117,66), thickness=1, circle_radius=3),
                #                         mp_drawing.DrawingSpec(color=(245,66,230), thickness=1, circle_radius=2)
                #                         )
                                
                cv2.imshow('Raw Webcam Feed', image)
                result.write(image) 
                # Break the loop if 'q' is pressed
                if cv2.waitKey(25) & 0xFF == ord('q'):
                    break

            # Release the VideoCapture and close the display window
            cap.release()

    # Exit the program
    result.release() 
    cv2.destroyAllWindows()



def save_files(video_files):
    farr = []

    for file in video_files:
        try:
            fc = VideoFileClip(os.path.join(video_dir, file))
            fc = fc.resize((1280,720))
            farr.append(fc)
        except Exception as e:
            print(file, e)
            continue
    
    fname = f"outputs/{uuid.uuid4()}.mp4"
    concatenate_videoclips(farr, method='compose').write_videofile(fname)
    return fname

