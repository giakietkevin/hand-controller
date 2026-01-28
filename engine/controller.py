from engine.utils import get_distance

class HandController:
    def __init__(self, click_threshold=30):
        self.click_threshold = click_threshold

    def get_gesture(self, landmarks):
        if len(landmarks) == 0:
            return None

        # Landmark 4: Ngón cái (Thumb), Landmark 8: Ngón trỏ (Index)
        thumb_tip = landmarks[4]
        index_tip = landmarks[8]
        middle_tip = landmarks[12]

        # Tính khoảng cách giữa ngón cái và ngón trỏ để xác định cú Click
        dist = get_distance(thumb_tip, index_tip)
        
        if dist < self.click_threshold:
            return "CLICK"
        
        # Nếu ngón trỏ giơ cao hơn các ngón khác -> Di chuyển
        if index_tip[1] < middle_tip[1]:
            return "MOVE"
            
        return "IDLE"