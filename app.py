import streamlit as st
import tempfile
from dotenv import load_dotenv
import os
from general_video.general import GeneralVideo
from general_video.multi_video import MultiVideo
from ai.gemini_util import Gemini
from ai.audio_util import Audio
from data_util.pexels_util import Pexels
from simple_app import simple_app
from advanced_app import advanced_app


# Load API Keys
load_dotenv()
gemini_api_key = os.getenv('GOOGLE_API_KEY')
pexels_api_key = os.getenv('PEXELS_API_KEY')

def main():
    st.title("Reel Generator")

    # Sidebar for mode selection
    st.sidebar.header("Settings")
    mode = st.sidebar.radio("Select Mode", ["Simple", "Advanced"])
    
    # Advanced settings dropdown (visible only if Advanced mode is selected)
    advanced_setting = None
    if mode == "Advanced":
        advanced_setting = st.sidebar.selectbox("Advanced Settings", ["Single Audio", "Multi Audio"])
    
    # Initialize Components
    llm = Gemini(api_key=gemini_api_key)
    audio = Audio()
    px = Pexels(pexels_api_key=pexels_api_key)
    
    if mode == "Simple":
        rg = GeneralVideo(llm, audio, px)
        simple_app(rg)
    else:
        rg = MultiVideo(llm, audio, px)
        advanced_app(rg, advanced_setting)

        

if __name__=='__main__':
    main()
