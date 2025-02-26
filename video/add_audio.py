import tempfile
from moviepy.editor import VideoFileClip, AudioFileClip

def add_audio_to_video(video_path: str, audio_path: str, output_path: str="samples/video_with_audio.mp4", temp: bool=True):
    """
    Adds an audio file to a video file, trims the video to match the audio duration, and saves the output.
    
    :param video_path: Path to the input video file.
    :param audio_path: Path to the input audio file.
    :param output_path: Path to save the output video file.
    :param temp: If True, saves the video in a temporary file and returns the file path.
    """
    # Load video and audio clips
    video = VideoFileClip(video_path)
    audio = AudioFileClip(audio_path)
    
    # Trim the video to match the audio duration
    video = video.subclip(0, min(video.duration, audio.duration))
    
    # Set the audio to the video
    video = video.set_audio(audio)
    
    if temp:
        temp_file = tempfile.NamedTemporaryFile(suffix=".mp4", delete=False)
        output_path = temp_file.name
    
    # Write the output file
    video.write_videofile(output_path, codec='libx264', audio_codec='aac')
    
    return output_path if temp else None


if __name__== '__main__':
    add_audio_to_video("final_video.mp4", "output.mp3", "audio_with_vidoe.mp4", temp=False)