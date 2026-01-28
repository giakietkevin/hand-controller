import cv2
import mediapipe as mp

class HandDetector:
    def __init__(self, mode=False, max_hands=1, model_complexity=0, detection_con=0.5, track_con=0.5):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=mode,
            max_num_hands=max_hands,
            model_complexity=model_complexity,
            min_detection_confidence=detection_con,
            min_tracking_confidence=track_con
        )
        self.mp_draw = mp.solutions.drawing_utils

    def findHands(self, img, draw=True):
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(img_rgb)
        all_landmarks = []

        if self.results.multi_hand_landmarks:
            for hand_lms in self.results.multi_hand_landmarks:
                if draw:
                    self.mp_draw.draw_landmarks(img, hand_lms, self.mp_hands.HAND_CONNECTIONS)
                
                # Trích xuất tọa độ pixel
                h, w, c = img.shape
                for id, lm in enumerate(hand_lms.landmark):
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    all_landmarks.append([cx, cy, lm.z])
        
        return img, all_landmarks