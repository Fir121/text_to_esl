import cv2
import os
from moviepy.editor import VideoFileClip, concatenate_videoclips, CompositeVideoClip
import mediapipe as mp
import numpy as np
import uuid

video_dir = 'videos/processed/'

def save_file_with_mediapipe(video_file):
    mp_drawing = mp.solutions.drawing_utils
    mp_hands = mp.solutions.hands
    mp_pose = mp.solutions.pose
    frame_width = frame_height = size = result = None
    with mp_hands.Hands(min_detection_confidence=0.4, min_tracking_confidence=0.4, model_complexity=0) as hands:
        with mp_pose.Pose(min_detection_confidence=0.4, min_tracking_confidence=0.4, model_complexity=0) as pose:
            cap = cv2.VideoCapture(video_file)
            
            if size is None:
                frame_width = int(cap.get(3)) 
                frame_height = int(cap.get(4)) 
                
                size = (frame_width, frame_height) 
                result = cv2.VideoWriter(f'{video_file.split(".")[0]}-1.mp4',  
                            cv2.VideoWriter_fourcc(*'MP4V'), 
                            cap.get(cv2.CAP_PROP_FPS), size) 

            # Play the video
            while True:
                ret, frame = cap.read()
                if not ret:
                    break

                # Recolor Feed
                image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                imagebg = np.zeros((image.shape[0], image.shape[1], 3), dtype = "uint8")
                # Make Detections
                results = hands.process(image)
                results2 = pose.process(image)

                # image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            
                if results.multi_hand_landmarks:
                    for hand_landmarks in results.multi_hand_landmarks:
                        mp_drawing.draw_landmarks(imagebg, hand_landmarks , mp_hands.HAND_CONNECTIONS, 
                                            mp_drawing.DrawingSpec(color=(121,22,76), thickness=2, circle_radius=3),
                                            mp_drawing.DrawingSpec(color=(121,44,250), thickness=2, circle_radius=3)
                                            )
                if results2.pose_landmarks:
                    # 17 - 22 set to null, to remove hand pose (overlaps with above)
                    for i in range(17,23):
                        del results2.pose_landmarks.landmark[i]
                        results2.pose_landmarks.landmark.insert(i,results2.pose_landmarks.landmark[30]) # hackiest hack of a solution to exist. Contact Firas to hear ;)
                    e_conn = set()
                    for conn in mp_pose.POSE_CONNECTIONS:
                        for j in range(17,23):
                            if j in conn:
                                break
                        else:
                            e_conn.add(conn)
                    mp_drawing.draw_landmarks(imagebg, results2.pose_landmarks , e_conn, 
                                    mp_drawing.DrawingSpec(color=(121,22,76), thickness=2, circle_radius=3),
                                    mp_drawing.DrawingSpec(color=(121,44,250), thickness=2, circle_radius=3)
                                    )
                                
                result.write(imagebg) 

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
    save_file_with_mediapipe(fname)

    mpipe = f'{fname.split(".")[0]}-1.mp4'

    vc1 = VideoFileClip(fname)
    vc2 = VideoFileClip(mpipe)

    # Crop the middle halves of the videos
    video1_cropped = vc1.crop(x1=320, x2=960)
    video2_cropped = vc2.crop(x1=320, x2=960)

    # Combine the videos side by side
    final_video = CompositeVideoClip([video1_cropped.set_position((0,0)), video2_cropped.set_position((640,0))], size=(1280,720))

    # Write the final video to a file
    final_video.write_videofile(f'{fname.split(".")[0]}-2.mp4')

    return f'{fname.split(".")[0]}-2.mp4'

