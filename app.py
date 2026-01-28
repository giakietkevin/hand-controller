import streamlit as st
from streamlit_webrtc import webrtc_streamer, WebRtcMode, RTCConfiguration
import cv2
import numpy as np
from engine.hand_tracking import HandDetector
from engine.controller import HandController

# STUN servers giúp WebRTC kết nối ổn định hơn
RTC_CONFIGURATION = RTCConfiguration(
    {"iceServers": [{"urls": ["stun:stun.l.google.com:19302", "stun:stun1.l.google.com:19302"]}]}
)

st.set_page_config(page_title="Hand Controller", layout="centered")
st.title("🎮 AI Virtual Mouse")

# Sử dụng cache để không khởi tạo lại model mỗi khi render
if 'detector' not in st.session_state:
    st.session_state.detector = HandDetector(model_complexity=0)
    st.session_state.controller = HandController()

def video_frame_callback(frame):
    img = frame.to_ndarray(format="bgr24")
    img = cv2.flip(img, 1)
    
    # Xử lý frame
    img, landmarks = st.session_state.detector.findHands(img)
    
    if landmarks:
        gesture = st.session_state.controller.get_gesture(landmarks)
        index_tip = landmarks[8]
        
        color = (0, 255, 0) if gesture == "CLICK" else (0, 0, 255)
        cv2.circle(img, (int(index_tip[0]), int(index_tip[1])), 12, color, cv2.FILLED)
        cv2.putText(img, f"Gesture: {gesture}", (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)

    return img

webrtc_streamer(
    key="hand-controller",
    mode=WebRtcMode.SENDRECV,
    rtc_configuration=RTC_CONFIGURATION,
    video_frame_callback=video_frame_callback,
    media_stream_constraints={"video": True, "audio": False},
    async_processing=True,
)