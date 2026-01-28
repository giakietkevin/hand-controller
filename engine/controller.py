import numpy as np

class HandController:
    def __init__(self, click_threshold=35):
        self.click_threshold = click_threshold

    def get_gesture(self, landmarks):
        if not landmarks: return "IDLE"

        # Tọa độ ngón cái (4) và ngón trỏ (8)
        thumb = np.array([landmarks[4][0], landmarks[4][1]])
        index = np.array([landmarks[8][0], landmarks[8][1]])

        # Tính khoảng cách Euclidean
        dist = np.linalg.norm(thumb - index)

        if dist < self.click_threshold:
            return "CLICK"
        return "MOVE"