import streamlit as st
from datetime import datetime
import cv2

st.set_page_config(
    page_title="Vision Inspec.",
    page_icon="🎥",
)

st.title("Vision Inspection 🎥")

st.write("test")

FRAME_WINDOW = st.image([])
camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)
isCapture = False

st.write("OKOK")

if st.button("촬영"):
    isCapture = True

while True:
    ret, frame = camera.read()
    if ret:
        if isCapture:
            fn = "photos/" + datetime.now().strftime("%Y%m%d_%H%M%S") + ".jpg"
            cv2.imwrite(fn, frame)
            isCapture = False
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        FRAME_WINDOW.image(frame)
