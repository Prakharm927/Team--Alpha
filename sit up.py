import cv2
import mediapipe as mp
from math import atan2, pi

# Initialize MediaPipe Pose
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()

# Function to detect sit-up pose
def detect_sit_up_pose(image):
    # Convert the image to RGB
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Process the image and get the pose landmarks
    results = pose.process(image_rgb)

    # Check if pose landmarks are detected
    if results.pose_landmarks:
        # Extract specific landmarks for sit-up pose correction
        nose_landmark = results.pose_landmarks.landmark[mp_pose.PoseLandmark.NOSE]
        hip_landmark = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_HIP]
        knee_landmark = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_KNEE]

        # Calculate angle between nose, hip, and knee landmarks
        angle = calculate_angle(nose_landmark, hip_landmark, knee_landmark)

        # Check if the angle is within the desired range for sit-up pose
        if 80 < angle < 100:
            return True, angle
        else:
            return False, angle
    else:
        return False, None

# Function to calculate angle between three landmarks
def calculate_angle(a, b, c):
    angle_rad = abs(atan2(c.y - b.y, c.x - b.x) - atan2(a.y - b.y, a.x - b.x))
    angle_deg = angle_rad * (180.0 / pi)
    return angle_deg

# Open a video capture stream
cap = cv2.VideoCapture(0)

while cap.isOpened():
    # Read a frame from the video stream
    ret, frame = cap.read()
    if not ret:
        break

    # Detect sit-up pose
    sit_up, angle = detect_sit_up_pose(frame)

    # Display the result on the frame
    if sit_up:
        cv2.putText(frame, f'Sit-up Pose Detected (Angle: {angle:.2f} degrees)', (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
    else:
        cv2.putText(frame, 'Not in Sit-up Pose', (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)

    # Display the frame
    cv2.imshow('Sit-up Pose Correction', frame)

    # Break the loop if 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture object
cap.release()

# Destroy all OpenCV windows
cv2.destroyAllWindows()
