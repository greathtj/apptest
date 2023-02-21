import streamlit as st
import datetime
import pandas as pd
import customLib as cl

st.set_page_config(
    page_title="유성레이저 IoT",
    page_icon="☄️",
)

st.title("유성레이저 설비 관리 V1.0")

st.header("Dashboard")

st.sidebar.header("설비 현황")