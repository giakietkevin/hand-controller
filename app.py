import streamlit as st
from streamlit_webrtc import webrtc_streamer, WebRtcMode, RTCConfiguration
import cv2
import numpy as np
# Import từ thư mục engine của bạn
from engine.hand_tracking import HandDetector 

# Cấu hình STUN server để WebRTC có thể đi xuyên tường lửa
RTC_CONFIGURATION = RTCConfiguration(
    {"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]}
)

st.title("AI Virtual Mouse - Hand Controller")
st.sidebar.title("Settings")
complexity = st.sidebar.slider("Model Complexity", 0, 1, 0)

# Khởi tạo Detector (giả sử lớp HandDetector trong engine của bạn nhận model_complexity)
detector = HandDetector(model_complexity=complexity)

def video_frame_callback(frame):
    img = frame.to_ndarray(format="bgr24")
    img = cv2.flip(img, 1) # Mirror effect
    
    # 1. Phát hiện tay (Sử dụng logic từ engine/hand_tracking.py)
    img, landmarks = detector.findHands(img)
    
    # 2. Logic điều khiển (Bạn có thể thêm từ engine/controller.py)
    if landmarks:
        # Ví dụ: Lấy tọa độ ngón trỏ (Landmark 8)
        index_finger = landmarks[8]
        cv2.circle(img, (int(index_finger[0]), int(index_finger[1])), 10, (0, 255, 0), cv2.FILLED)

    return img

webrtc_streamer(
    key="hand-controller",
    mode=WebRtcMode.SENDRECV,
    rtc_configuration=RTC_CONFIGURATION,
    video_frame_callback=video_frame_callback,
    media_stream_constraints={"video": True, "audio": False},
    async_processing=True,
)