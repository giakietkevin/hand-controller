import numpy as np

class KalmanFilter:
    """Bộ lọc đơn giản để giảm rung cho con trỏ chuột"""
    def __init__(self, alpha=0.5):
        self.alpha = alpha
        self.prev_val = None

    def apply(self, current_val):
        if self.prev_val is None:
            self.prev_val = current_val
        smoothed_val = self.alpha * np.array(current_val) + (1 - self.alpha) * np.array(self.prev_val)
        self.prev_val = smoothed_val
        return smoothed_val

def get_distance(p1, p2):
    """Tính khoảng cách Euclidean giữa 2 điểm"""
    return np.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)