import cv2
import mediapipe as mp
from utils import *
from body_part_angle import BodyPartAngle
from types_of_exercise import TypeOfExercise

# Get exercise type from user
exercise_type = input("Enter the type of exercise: ")

# Get video source from user
video_source = input("Enter the full video path (Enter 'webcam' for webcam): ")

if video_source.lower() == 'webcam':
    cap = cv2.VideoCapture(0)  # webcam
else:
    cap = cv2.VideoCapture(video_source)

if not cap.isOpened():
    print(f"Error opening video source: {video_source}")
    exit()

cap.set(3, 800)  # width
cap.set(4, 480)  # height

# setup mediapipe
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    counter = 0  # movement of exercise
    status = True  # state of move
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("Error reading frame.")
            break
        frame = cv2.resize(frame, (800, 480), interpolation=cv2.INTER_AREA)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame.flags.writeable = False
        results = pose.process(frame)
        frame.flags.writeable = True
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

        try:
            landmarks = results.pose_landmarks.landmark
            counter, status = TypeOfExercise(landmarks).calculate_exercise(
                exercise_type, counter, status)
        except Exception as e:
            print(f"Error processing pose: {e}")

        frame = score_table(exercise_type, frame, status)

        mp_drawing.draw_landmarks(
            frame,
            results.pose_landmarks,
            mp_pose.POSE_CONNECTIONS,
            mp_drawing.DrawingSpec(color=(255, 255, 255),
                                   thickness=2,
                                   circle_radius=2),
            mp_drawing.DrawingSpec(color=(174, 139, 45),
                                   thickness=2,
                                   circle_radius=2),
        )

        cv2.imshow('Video', frame)
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
