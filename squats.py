import cv2
import mediapipe as mp
import math

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

def calculate_angle(a, b, c):
    angle_rad = abs(math.atan2(c.y - b.y, c.x - b.x) - math.atan2(a.y - b.y, a.x - b.x))
    angle_deg = math.degrees(angle_rad)
    return angle_deg

def detect_squat_posture(image):
    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        # Convert the image to RGB
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        # Process the image and get the pose results
        results = pose.process(image_rgb)
        
        # Draw landmarks on the image
        if results.pose_landmarks:
            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
            
            # Check squat posture based on landmarks
            left_hip = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_HIP]
            right_hip = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_HIP]
            left_knee = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_KNEE]
            right_knee = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_KNEE]
            
            # Calculate the angle between the hips and knees
            angle_left = calculate_angle(left_hip, left_knee, results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_ANKLE])
            angle_right = calculate_angle(right_hip, right_knee, results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_ANKLE])
            
            # Check if the angles suggest a proper squat posture
            if 100 < angle_left < 160 and 100 < angle_right < 160:
                cv2.putText(image, "Correct Squat Posture", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
                cv2.putText(image, "Keep it up!", (50, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2, cv2.LINE_AA)
            else:
                cv2.putText(image, "Incorrect Squat Posture", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
                
                # Provide feedback on adjustments
                if angle_left < 100:
                    cv2.putText(image, "Adjust left knee position", (50, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2, cv2.LINE_AA)
                elif angle_left > 160:
                    cv2.putText(image, "Adjust left knee position", (50, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2, cv2.LINE_AA)
                
                if angle_right < 100:
                    cv2.putText(image, "Adjust right knee position", (50, 110), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2, cv2.LINE_AA)
                elif angle_right > 160:
                    cv2.putText(image, "Adjust right knee position", (50, 110), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2, cv2.LINE_AA)
    
    return image

# Example usage with webcam feed
cap = cv2.VideoCapture(0)  # Use 0 for the default camera

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    
    frame = detect_squat_posture(frame)
    
    cv2.imshow('Squat Posture Detector', frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

