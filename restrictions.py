import cv2
import mediapipe as mp
import math

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

def detect_pushup_pose(image):
    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        # Convert the image to RGB
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        # Process the image and get the pose results
        results = pose.process(image_rgb)
        
        # Draw landmarks on the image
        if results.pose_landmarks:
            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
            
            # Check push-up pose based on landmarks
            left_shoulder = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER]
            right_shoulder = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER]
            left_elbow = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_ELBOW]
            right_elbow = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_ELBOW]
            
            # Calculate the angle between the shoulders and elbows
            angle_left = calculate_angle(left_shoulder, left_elbow, results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_WRIST])
            angle_right = calculate_angle(right_shoulder, right_elbow, results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_WRIST])
            
            # Check if the angles suggest a push-up pose
            if 60 < angle_left < 120 and 60 < angle_right < 120:
                # Additional checks, if needed
                # For example, you can check the position of other body parts
                
                # Display push-up pose
                cv2.putText(image, "Push-up Pose", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
            else:
                # Display message for incorrect pose
                cv2.putText(image, "Incorrect Pose", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
    
    return image

def calculate_angle(a, b, c):
    angle_rad = abs(math.atan2(c.y - b.y, c.x - b.x) - math.atan2(a.y - b.y, a.x - b.x))
    angle_deg = math.degrees(angle_rad)
    return angle_deg

# Example usage
cap = cv2.VideoCapture(0)  # Use 0 for the default camera

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    
    frame = detect_pushup_pose(frame)
    
    cv2.imshow('Push-up Pose Detector', frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
