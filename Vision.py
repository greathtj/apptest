import streamlit as st
from streamlit_webrtc import webrtc_streamer

st.title("Web Cam Test")
webrtc_streamer(key="sample")
