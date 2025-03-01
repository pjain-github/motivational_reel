
import streamlit as st
import tempfile
from general_video.general import GeneralVideo
from ai.gemini_util import Gemini
from ai.audio_util import Audio
from data_util.pexels_util import Pexels
from dotenv import load_dotenv
import os

# Load API Keys
load_dotenv()
gemini_api_key = os.getenv('GOOGLE_API_KEY')
pexels_api_key = os.getenv('PEXELS_API_KEY')

# Initialize Components
llm = Gemini(api_key=gemini_api_key)
audio = Audio()
px = Pexels(pexels_api_key=pexels_api_key)
rg = GeneralVideo(llm, audio, px)

st.title("Reel Generator")

# Initialize session state if not present
if "text_input" not in st.session_state:
    st.session_state.text_input = None
if "audio_path" not in st.session_state:
    st.session_state.audio_path = None
if "wps" not in st.session_state:
    st.session_state.wps = 1.5  # Default value
if "subtitle_video_path" not in st.session_state:
    st.session_state.subtitle_video_path = None
if "subtitle_path" not in st.session_state:
    st.session_state.subtitle_path = None
if "background_music" not in st.session_state:
    st.session_state.background_music = None
if "video_path" not in st.session_state:
    st.session_state.video_path = None
if "final_video_path" not in st.session_state:
    st.session_state.final_video_path = None

# Section 1: Audio Generator
with st.expander("Audio Section", expanded=False):
    text_input = st.text_area("Enter Text for Audio")
    if text_input:
        st.session_state.text_input = text_input

    pitch = st.slider("Pitch Adjustment (Hz)", -30, 30, 0)
    speed = st.slider("Speed Adjustment (%)", -50, 50, 0)

    pitch = f"{pitch}Hz" if pitch != 0 else None
    speed = f"{speed}%" if speed != 0 else None

    # Generate Audio
    if st.button("Generate Audio"):
        audio_path, _, wps = rg.generate_audio(text_input, speed, pitch)
        
        if not audio_path:
            st.error("Error generating audio. Check your input or API settings.")
        else:
            st.session_state.audio_path = audio_path
            st.session_state.wps = round(wps, 1)
            st.session_state.subtitle_video_path = None
            st.success("Audio generated successfully!")
    
    # Display audio if it exists
    if st.session_state.audio_path:
        st.audio(st.session_state.audio_path, format='audio/mp3')
        st.write(f"Words per second: {st.session_state.wps}")
        
        wps_slider = st.slider("Words per second", 0.5, 4.0, st.session_state.wps, key="wps_slider")

        # Generate Subtitles
        if st.button("Generate Subtitles"):
            subtitle_video_path, subtitle_path = rg.test_subtitles(
                quote=text_input, 
                audio_path=st.session_state.audio_path, 
                words_per_sec=wps_slider
            )

            if not subtitle_video_path:
                st.error("Error generating subtitle video. Check the logs.")
            else:
                st.session_state.subtitle_video_path = subtitle_video_path
                st.session_state.subtitle_path = subtitle_path
                st.success("Subtitle video generated successfully!")

    # Display subtitle video if it exists
    if st.session_state.subtitle_video_path:
        st.video(st.session_state.subtitle_video_path)


# Section 2: Background Music
with st.expander("Background Music", expanded=False):
    uploaded_music = st.file_uploader("Upload your background music file", type=["mp3", "wav"])

    if uploaded_music:
        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{uploaded_music.name.split('.')[-1]}") as temp_file:
            temp_file.write(uploaded_music.read())
            temp_music_path = temp_file.name

        st.session_state.background_music = temp_music_path
        st.success("Background music uploaded successfully!")
    
    # Play the uploaded background music
    if st.session_state.background_music:
        st.audio(st.session_state.background_music, format="audio/mp3")

# Section 3: Video Generation
with st.expander("Video Section", expanded=False):
    video_url = st.text_input("Enter the URL of the video you want to use")

    # Handle Video URL Download
    if video_url:
        if st.button("Download Video"):
            video_path = rg.pull_video(video_url)  # Function to download video
            if video_path:
                st.session_state.video_path = video_path
                st.success("Video downloaded successfully!")
            else:
                st.error("Failed to download video. Check the URL.")

    # File uploader for video
    uploaded_video = st.file_uploader("Upload your video file", type=["mp4"])

    if uploaded_video:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_file:
            temp_file.write(uploaded_video.read())
            temp_video_path = temp_file.name

        st.session_state.video_path = temp_video_path
        st.success("Video uploaded successfully!")

    # Display video if available
    if st.session_state.video_path:
        st.markdown(
            f"""
            <style>
                video {{
                    max-height: 400px; /* Limit video height */
                    width: auto;
                    display: block;
                    margin: auto;
                }}
            </style>
            """,
            unsafe_allow_html=True,
        )
        st.video(st.session_state.video_path)

# Final Video Generation Button
st.markdown("---")

if st.button("Generate Final Video"):
    # Check if all required files are available
    if not st.session_state.audio_path:
        st.error("Missing Audio. Please generate audio first.")
    elif not st.session_state.background_music:
        st.error("Missing Background Music. Please upload a background music file.")
    elif not st.session_state.video_path:
        st.error("Missing Video. Please upload or download a video.")
    else:
        st.success("All files available! Generating final video...")
        
        # Generate the final video
        final_video_path = rg.generate_video(quote=st.session_state.text_input, 
                                             audio_path=st.session_state.audio_path,
                                             video_path=st.session_state.video_path, 
                                             subtitle_path=st.session_state.subtitle_path, 
                                             music=st.session_state.background_music)

        if final_video_path:
            st.session_state.final_video_path = final_video_path
            st.success("Final video generated successfully!")
        else:
            st.error("Error generating the final video.")

# Display the final video if available
if st.session_state.final_video_path:
    st.markdown(
        f"""
        <style>
            video {{
                max-height: 400px; /* Limit video height */
                width: auto;
                display: block;
                margin: auto;
            }}
        </style>
        """,
        unsafe_allow_html=True,
    )
    st.video(st.session_state.final_video_path)
