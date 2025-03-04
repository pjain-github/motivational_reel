from video import add_audio, add_music, add_subtitles
from moviepy.editor import VideoFileClip, concatenate_videoclips, vfx
import tempfile

def combine_video(input_video_path, audio_path, subtitle_path, music_path=None):

    video = add_subtitles.add_subtitles_to_video(video_path=input_video_path, subtitle_path=subtitle_path)

    video = add_audio.add_audio_to_video(video_path=video, audio_path=audio_path)

    if music_path:
        video = add_music.add_background_music(video_path=video, music_path=music_path, temp=True)

    return video

# def merge_video(video_paths, height=1920, width=1080, output_path="samples/merged_video.mp4", temp=True):
#     clips = []
#     for path in video_paths:
#         clip = VideoFileClip(path)
#         aspect_ratio = clip.w / clip.h
#         new_width = int(height * aspect_ratio)
#         resized_clip = clip.resize(height=height)
        
#         # Adding fade-in and fade-out
#         faded_clip = resized_clip.fadein(0.5).fadeout(0.5)
#         clips.append(faded_clip)
    
#     # Apply crossfade transition manually
#     for i in range(len(clips) - 1):
#         clips[i] = clips[i].crossfadeout(0.5)
#         clips[i + 1] = clips[i + 1].crossfadein(0.5)
    
#     final_clip = concatenate_videoclips(clips, method="compose")
    
#     if temp:
#         temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
#         output_path = temp_file.name
#         temp_file.close()
    
#     final_clip.write_videofile(output_path, codec="libx264", audio_codec="aac")
    
#     print(f"Video saved at {output_path}")
#     return output_path

def merge_video(video_paths, height=1920, width=1080, output_path="samples/merged_video.mp4", temp=True):
    clips = []
    for path in video_paths:
        clip = VideoFileClip(path)
        aspect_ratio = clip.w / clip.h
        new_width = int(height * aspect_ratio)
        resized_clip = clip.resize(height=height)
        
        # Crop if width exceeds max width
        if new_width > width:
            x_center = new_width // 2
            x1 = x_center - (width // 2)
            x2 = x_center + (width // 2)
            resized_clip = resized_clip.crop(x1=x1, width=width)
        
        # Adding fade-in and fade-out
        faded_clip = resized_clip.fadein(0.5).fadeout(0.5)
        clips.append(faded_clip)
    
    # Apply crossfade transition manually
    for i in range(len(clips) - 1):
        clips[i] = clips[i].crossfadeout(0.5)
        clips[i + 1] = clips[i + 1].crossfadein(0.5)
    
    final_clip = concatenate_videoclips(clips, method="compose")
    
    if temp:
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
        output_path = temp_file.name
        temp_file.close()
    
    final_clip.write_videofile(output_path, codec="libx264", audio_codec="aac")
    
    print(f"Video saved at {output_path}")
    return output_path