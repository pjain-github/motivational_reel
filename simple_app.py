import streamlit as st
import tempfile

def simple_app(rg):

    # Initialize session state if not present
    for key in ["text_input", "audio_path", "background_music", "video_path", "final_video_path"]:
        if key not in st.session_state:
            st.session_state[key] = None
    
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
            audio_path = rg.generate_audio(text_input, speed, pitch)
            if not audio_path:
                st.error("Error generating audio. Check your input or API settings.")
            else:
                st.session_state.audio_path = audio_path
                st.success("Audio generated successfully!")
        
        if st.session_state.audio_path:
            st.audio(st.session_state.audio_path, format='audio/mp3')
    
    # Section 2: Background Music
    with st.expander("Background Music", expanded=False):
        uploaded_music = st.file_uploader("Upload your background music file", type=["mp3", "wav"])
        
        if uploaded_music:
            with tempfile.NamedTemporaryFile(delete=False, suffix=f".{uploaded_music.name.split('.')[-1]}") as temp_file:
                temp_file.write(uploaded_music.read())
                st.session_state.background_music = temp_file.name
                st.success("Background music uploaded successfully!")
        
        if st.session_state.background_music:
            st.audio(st.session_state.background_music, format="audio/mp3")
    
    # Section 3: Video Generation
    with st.expander("Video Section", expanded=False):
        video_url = st.text_input("Enter the URL of the video you want to use")
        
        if video_url and st.button("Download Video"):
            video_path = rg.pull_video(video_url)
            if video_path:
                st.session_state.video_path = video_path
                st.success("Video downloaded successfully!")
            else:
                st.error("Failed to download video. Check the URL.")
        uploaded_video = st.file_uploader("Upload your video file", type=["mp4"])
        
        if uploaded_video:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_file:
                temp_file.write(uploaded_video.read())
                st.session_state.video_path = temp_file.name
                st.success("Video uploaded successfully!")
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
    
    st.markdown("---")
    
    if st.button("Generate Final Video"):
        if not st.session_state.audio_path:
            st.error("Missing Audio. Please generate audio first.")
        elif not st.session_state.background_music:
            st.error("Missing Background Music. Please upload a background music file.")
        elif not st.session_state.video_path:
            st.error("Missing Video. Please upload or download a video.")
        else:
            st.success("All files available! Generating final video...")
            final_video_path = rg.generate_video(
                audio_path=st.session_state.audio_path,
                video_path=st.session_state.video_path,
                music=st.session_state.background_music,
            )
            if final_video_path:
                st.session_state.final_video_path = final_video_path
                st.success("Final video generated successfully!")
            else:
                st.error("Error generating the final video.")
    
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