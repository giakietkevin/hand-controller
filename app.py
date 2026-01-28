import streamlit as st
from streamlit_webrtc import webrtc_streamer, WebRtcMode, RTCConfiguration
import cv2
import numpy as np

# --- THAY ĐỔI Ở ĐÂY: Import trực tiếp, không qua engine ---
from hand_tracking import HandDetector
from controller import HandController
# ---------------------------------------------------------

# Cấu hình STUN Server
RTC_CONFIGURATION = RTCConfiguration(
    {"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]}
)

st.set_page_config(page_title="Hand Controller", layout="centered")
st.title("🎮 AI Virtual Mouse")

# Khởi tạo model
if 'detector' not in st.session_state:
    st.session_state.detector = HandDetector(model_complexity=0)
    st.session_state.controller = HandController()

def video_frame_callback(frame):
    img = frame.to_ndarray(format="bgr24")
    img = cv2.flip(img, 1) # Lật ảnh như gương
    
    # Phát hiện tay
    img, landmarks = st.session_state.detector.findHands(img)
    
    if landmarks:
        # Lấy cử chỉ
        gesture = st.session_state.controller.get_gesture(landmarks)
        index_tip = landmarks[8]
        
        # Vẽ giao diện
        color = (0, 255, 0) if gesture == "CLICK" else (0, 0, 255)
        cv2.circle(img, (int(index_tip[0]), int(index_tip[1])), 15, color, cv2.FILLED)
        cv2.putText(img, f"Mode: {gesture}", (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)

    return img

webrtc_streamer(
    key="hand-controller",
    mode=WebRtcMode.SENDRECV,
    rtc_configuration=RTC_CONFIGURATION,
    video_frame_callback=video_frame_callback,
    media_stream_constraints={"video": True, "audio": False},
    async_processing=True,
)