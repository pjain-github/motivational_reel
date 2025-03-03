import streamlit as st
import os 
import tempfile

def final_video(rg, advanced_setting):

    if advanced_setting == "Single Audio":

        # Section 1: Audio Generator
        with st.expander("Audio Section", expanded=False):

            text_input = st.text_area("Enter Text for Audio")
            if text_input:
                st.session_state.final_text_input = text_input

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
                    st.session_state.final_audio_path = audio_path
                    st.success("Audio generated successfully!")

            if st.session_state.final_audio_path:
                st.audio(st.session_state.final_audio_path, format='audio/mp3')
    
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

    st.markdown("---")

    def check_uploaded(video_no):
        if advanced_setting == "Single Audio":
            return st.session_state.video_paths[video_no]["video_path"] is not None
        else:
            return st.session_state.video_paths[video_no]["video_path"] is not None and st.session_state.video_paths[video_no]["audio_path"] is not None

    def get_video_list():
        return [f"Video {i+1} " + ("✅" if check_uploaded(i) else "❌") for i in range(len(st.session_state.video_paths))]


    uploaded_videos = get_video_list()
    st.write("Uploaded Videos:")
    for video in uploaded_videos:
        st.write(video)

    if all("✅" in video for video in uploaded_videos):
        st.write("All videos uploaded successfully!")

    if st.button("Generate Final Video"):

        if advanced_setting == "Single Audio":

            if not st.session_state.final_audio_path:
                st.error("Missing Audio. Please generate audio first.")
            elif not st.session_state.background_music:
                st.error("Missing Background Music. Please upload a background music file.")
            elif not all(st.session_state.video_paths[i]["video_path"] for i in range(len(st.session_state.video_paths))):
                st.error("Missing Video. Please upload or download a video.")
            else:
                st.success("All files available! Generating final video...")
                final_video_path = rg.generate_multi_video_simple(
                    audio_path=st.session_state.final_audio_path,
                    video_paths=[st.session_state.video_paths[i]["video_path"] for i in range(len(st.session_state.video_paths))],
                    music=st.session_state.background_music
                )
                if final_video_path:
                    st.session_state.final_video_path = final_video_path
                    st.success("Final video generated successfully!")
                else:
                    st.error("Error generating the final video.")

        else:

            if not st.session_state.background_music:
                st.error("Missing Background Music. Please upload a background music file.")
            elif not all(st.session_state.video_paths[i]["video_path"] for i in range(len(st.session_state.video_paths))):
                st.error("Missing Video. Please upload or download a video.")
            elif not all(st.session_state.video_paths[i]["audio_path"] for i in range(len(st.session_state.video_paths))):
                st.error("Missing Audio. Please generate audio for all videos.")
            else:
                st.success("All files available! Generating final video...")
                final_video_path = rg.generate_multi_video(
                    data_list=st.session_state.video_paths,
                    music=st.session_state.background_music
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
    

def video_section(rg, advanced_setting, selected_video):

    if advanced_setting == "Multi Audio":
        # Section 1: Audio Section

        with st.expander("Audio Section", expanded=False):
        
            text_input = st.text_area("Enter Text for Audio")
            if text_input:
                st.session_state.video_paths[selected_video]['text_input'] = text_input            
            
            pitch = st.slider("Pitch Adjustment (Hz)", -30, 30, 0)
            speed = st.slider("Speed Adjustment (%)", -50, 50, 0)
            pitch = f"{pitch}Hz" if pitch != 0 else None
            speed = f"{speed}%" if speed != 0 else None
            
            # Generate Audio
            if st.button("Generate Audio"):
                audio_path = rg.generate_audio(st.session_state.video_paths[selected_video]['text_input'], speed, pitch)
                if not audio_path:
                    st.error("Error generating audio. Check your input or API settings.")
                else:
                    st.session_state.video_paths[selected_video]['audio_path'] = audio_path
                    st.success("Audio generated successfully!")         
            
            if st.session_state.video_paths[selected_video]['audio_path']:
                st.audio(st.session_state.video_paths[selected_video]['audio_path'], format='audio/mp3')

    # Section 2: Video Generation
    with st.expander("Video Section", expanded=False):
        
        type = st.selectbox("Upload", ["Video", "Image"])

        if type=="Video":

            url = st.text_input("Enter the URL of the video you want to use")

            if url and st.button("Download Video"):
                video_path = rg.pull_video(url)
                if video_path:
                    st.session_state.video_paths[selected_video]['video_path'] = video_path
                    st.success("Video downloaded successfully!")
                else:
                    st.error("Failed to download video. Check the URL.")

                url = None
                st.rerun()

            uploaded_file = st.file_uploader("Upload your video file", type=["mp4"], key=f"uploader_{st.session_state.uploaded_file_key}")

            if uploaded_file:
                with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_file:
                    temp_file.write(uploaded_file.read())
                    st.session_state.video_paths[selected_video]['video_path'] = temp_file.name
                    st.success("Video uploaded successfully!")
                
                st.session_state.uploaded_file_key+= 1
                st.rerun()

        elif type=="Image":
            url = st.text_input("Enter the URL of the image you want to use")

            if url and st.button("Download Image"):
                video_path = rg.pull_image(url, time=st.session_state.video_paths[selected_video]['audio_time'])
                if video_path:
                    st.session_state.video_paths[selected_video]['video_path'] = video_path
                    st.success("Video downloaded successfully!")
                else:
                    st.error("Failed to download video. Check the URL.")
            
            uploaded_file = st.file_uploader("Upload your image file", type=["jpg", "jpeg", "png", "webp"], key=f"uploader_{st.session_state.uploaded_file_key}")

            if uploaded_file:

                ext = os.path.splitext(uploaded_file.name)[-1].lower()
                if ext not in [".jpg", ".jpeg", ".webp", ".png"]:
                    ext = ".png"

                with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as temp_file:
                    temp_file.write(uploaded_file.read())
                    video_path = rg.get_video_from_image(image_path=temp_file.name, time=st.session_state.video_paths[selected_video]['audio_time'])
                    st.session_state.video_paths[selected_video]['video_path'] = video_path
                    st.success("Video generated successfully!")

                st.session_state.uploaded_file_key+= 1
                st.rerun()

        if st.session_state.video_paths[selected_video]['video_path']:
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
            st.video(st.session_state.video_paths[selected_video]['video_path'])


def advanced_app(rg, advanced_setting):
    # Initialize session state if not present
    for key in ["final_text_input", "final_audio_path", "background_music", "video_paths", "final_video_path", "selected_video"]:
        if key not in st.session_state:
            st.session_state[key] = None
            if key == "video_paths":
                st.session_state.video_paths = []
                st.session_state.video_paths.append({
                    "text_input": None, 
                    "audio_path": None, 
                    "video_path": None, 
                    "audio_time": 5})
            if key == "selected_video":
                st.session_state.selected_video = 0

    # Ensure rerun flag exists
    if "rerun_needed" not in st.session_state:
        st.session_state["rerun_needed"] = False
    
    if "uploaded_file_key" not in st.session_state: 
        st.session_state.uploaded_file_key = 0

    def check_uploaded(video_no):
        if advanced_setting == "Single Audio":
            return st.session_state.video_paths[video_no]["video_path"] is not None
        else:
            return st.session_state.video_paths[video_no]["video_path"] is not None and st.session_state.video_paths[video_no]["audio_path"] is not None


    def get_video_list():
        return [f"Video {i+1} " + ("✅" if check_uploaded(i) else "❌") for i in range(len(st.session_state.video_paths))]

    page = st.sidebar.radio("Select Page", ["Final Video", "Video Upload"])

    if page == "Video Upload":
        st.header("Video Upload")

        col1, col2 = st.columns([1, 1])
        
        updated = False  # Flag to check if changes are made

        def update_selected_video():
            st.session_state["rerun_needed"] = True  # Mark rerun request

        video_selected = st.selectbox(
            "List of Videos", 
            get_video_list(), 
            index=st.session_state.selected_video, 
            key="video_dropdown",
            on_change=update_selected_video)
        
        if st.session_state["rerun_needed"]:
            st.session_state["rerun_needed"] = False  # Reset the flag
            st.rerun()
        
        with col1:
            if st.button("Add Video"):
                st.session_state.video_paths.append({"text_input": None, "audio_path": None, "video_path": None, "audio_time": 5})
                st.session_state.selected_video = len(st.session_state.video_paths) - 1
                updated = True
                st.success("Video added successfully!")

        with col2:
            if st.button(f"Delete Video {st.session_state.selected_video + 1}"):
                if len(st.session_state.video_paths) > 1:
                    st.session_state.video_paths.pop(st.session_state.selected_video)
                    st.session_state.selected_video = max(0, st.session_state.selected_video - 1)
                    updated = True
                    st.success("Video deleted successfully!")
                else:
                    st.error("At least one video must be present.")

        # Force update dropdown after add/delete action
        if updated:
            st.rerun()
        
        if st.session_state.selected_video!=None:

            selected_video = int(video_selected.split(" ")[1]) - 1
        
            if selected_video != st.session_state.selected_video:
                st.session_state.selected_video = selected_video
                st.rerun()
            
            video_section(rg, advanced_setting, st.session_state.selected_video)

        else:
            print("************")
            print(st.session_state.selected_video)
            print(int(video_selected.split(" ")[1]) - 1)
            st.warning("No videos uploaded. Click 'Add Video' to upload a video.")

        
    if page == "Final Video":
        st.header("Final Video")

        final_video(rg, advanced_setting)
    

    
