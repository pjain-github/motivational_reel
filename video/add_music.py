import tempfile
from moviepy.editor import VideoFileClip, AudioFileClip, CompositeAudioClip


def add_background_music(video_path: str, music_path: str, output_path: str="samples/video_with_music.mp4", temp: bool=True):
    """
    Adds background music to a video file, keeping the original audio, trimming the music to match the video duration, 
    lowering the background music volume, and saves the output.
    
    :param video_path: Path to the input video file.
    :param music_path: Path to the background music file.
    :param output_path: Path to save the output video file.
    :param temp: If True, saves the video in a temporary file and returns the file path.
    """
    # Load video and music clips
    video = VideoFileClip(video_path)
    original_audio = video.audio
    music = AudioFileClip(music_path).subclip(0, video.duration).volumex(0.3)  # Lower music volume
    
    # Combine original audio and background music
    final_audio = CompositeAudioClip([original_audio, music])
    video = video.set_audio(final_audio)
    
    if temp:
        temp_file = tempfile.NamedTemporaryFile(suffix=".mp4", delete=False)
        output_path = temp_file.name
    
    # Write the output file
    video.write_videofile(output_path, codec='libx264', audio_codec='aac')
    
    return output_path if temp else None

if __name__=='__main__':
    add_background_music("audio_with_vidoe.mp4", "sample_background_music.mp3", "video_with_music.mp4", temp=False)