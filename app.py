import pandas as pd
import streamlit as st

uploadedFiles = st.file_uploader(
    "Upload videos", accept_multiple_files=True, type="mp4"
)