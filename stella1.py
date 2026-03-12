import cv2
import mediapipe as mp
import pyautogui
import time

# --- SAFETY FEATURE ---
# If the mouse goes crazy, slam it to the top-left corner of the screen to kill the program.
pyautogui.FAILSAFE = True 

# 1. SETUP THE CAMERA & AI
cap = cv2.VideoCapture(0) # 0 is usually the default webcam
hand_detector = mp.solutions.hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
drawing_utils = mp.solutions.drawing_utils
screen_width, screen_height = pyautogui.size()

# Smoothing variables (makes the mouse movement look professional, not shaky)
prev_x, prev_y = 0, 0
curr_x, curr_y = 0, 0
smoothening = 5 

def draw_hud(image, fps):
    """Draws the VIP 'System Interface' overlay"""
    # Create a black bar at the top
    cv2.rectangle(image, (0, 0), (640, 60), (0, 0, 0), -1) 
    # Add text
    cv2.putText(image, f"SYSTEM: ONLINE | FPS: {int(fps)}", (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
    cv2.putText(image, "MODE: GESTURE CONTROL", (10, 45), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1)
    return image

print("--- INITIALIZING JARVIS INTERFACE ---")
print("Press 'q' in the camera window to stop.")

pTime = 0

while True:
    success, frame = cap.read()
    if not success:
        print("Error: Camera not found.")
        break

    # Flip the frame so it acts like a mirror (easier to control)
    frame = cv2.flip(frame, 1) 
    frame_height, frame_width, _ = frame.shape
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # 2. AI PROCESSING
    output = hand_detector.process(rgb_frame)
    hands = output.multi_hand_landmarks
    
    # Calculate FPS
    cTime = time.time()
    fps = 1 / (cTime - pTime) if (cTime - pTime) > 0 else 0
    pTime = cTime
    
    frame = draw_hud(frame, fps)

    if hands:
        for hand in hands:
            # Draw the Skeleton
            drawing_utils.draw_landmarks(frame, hand)
            
            landmarks = hand.landmark
            for id, landmark in enumerate(landmarks):
                x = int(landmark.x * frame_width)
                y = int(landmark.y * frame_height)
                
                # Logic: Index Finger Tip (ID 8) moves the mouse
                if id == 8:
                    cv2.circle(frame, (x, y), 10, (0, 255, 0), cv2.FILLED)
                    
                    # Convert camera coordinates to screen coordinates
                    curr_x = prev_x + (x * screen_width // frame_width - prev_x) / smoothening
                    curr_y = prev_y + (y * screen_height // frame_height - prev_y) / smoothening
                
                    # Move Mouse
                    pyautogui.moveTo(curr_x, curr_y)
                    prev_x, prev_y = curr_x, curr_y

                # Logic: Thumb Tip (ID 4) triggers click
                if id == 4:
                    thumb_x, thumb_y = x, y
                    cv2.circle(frame, (x, y), 10, (255, 0, 255), cv2.FILLED)
                    
                    # If Thumb is close to Index Vertical position -> Click
                    if abs(curr_y - (thumb_y * screen_height // frame_height)) < 30:
                        cv2.putText(frame, "CLICK!", (50, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
                        pyautogui.click()
                        pyautogui.sleep(0.2) 

    cv2.imshow('AI Control - President Demo', frame)
    
    # Press 'q' to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()