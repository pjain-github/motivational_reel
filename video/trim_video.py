import tempfile
import moviepy.editor as mp

def trim_video(video_path: str, time: float) -> str:
    """
    Trims the input video to the specified duration and replaces the original file.
    
    :param video_path: Path to the input video file.
    :param time: Duration (in seconds) to keep from the start of the video.
    :return: Path to the trimmed video file.
    """
    # Load the video file
    video = mp.VideoFileClip(video_path)
    
    # Trim the video to the specified duration
    trimmed_video = video.subclip(0, min(time, video.duration))
    
    # Save the trimmed video to the original file path
    trimmed_video.write_videofile(video_path, codec="libx264", audio_codec="aac")
    
    return video_path

