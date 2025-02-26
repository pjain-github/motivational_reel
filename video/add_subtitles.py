import tempfile
from moviepy.editor import VideoFileClip, ImageClip, concatenate_videoclips, CompositeVideoClip
from PIL import Image, ImageDraw, ImageFont
import pysrt
import os

def add_subtitles_to_video(
        video_path: str,
        subtitle_path: str,
        output_video_path: str = "samples/output_with_subtitles.mp4",
        font_path: str = "fonts/freesans-font/FreeSans-LrmZ.ttf",
        temp: bool = True
    ) -> str:
    """
    Overlays subtitles onto an existing video.
    
    :param video_path: Path to the input video file
    :param subtitle_path: Path to the subtitle (.srt) file
    :param output_video_path: Path to save the output video
    :param font_path: Path to the font file (optional)
    :param temp: If True, saves the video in a temporary file
    :return: Path of the saved video file
    """
    # Load video
    video = VideoFileClip(video_path)
    video_width, video_height = video.size
    fps = video.fps

    # Load subtitles
    subs = pysrt.open(subtitle_path)

    # Function to create subtitle images
    def create_subtitle_image(text):
        """Creates an image with subtitles centered."""
        img = Image.new("RGBA", (video_width, video_height), (0, 0, 0, 0))  # Transparent background
        draw = ImageDraw.Draw(img)
        
        font_size = video_height // 20
        try:
            font = ImageFont.truetype(font_path, size=font_size) if font_path else ImageFont.load_default()
        except:
            font = ImageFont.load_default()
        
        text_w, text_h = draw.textbbox((0, 0), text, font=font)[2:]
        x = (video_width - text_w) // 2
        y = (video_height - text_h) // 2
        
        # draw.rectangle([x - 5, y - 3, x + text_w + 5, y + text_h + 3], fill="grey")
        draw.text((x, y), text, font=font, fill="white")

        return img

    # Create subtitle clips
    subtitle_clips = []

    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
    temp_img_path = temp_file.name
    temp_file.close()
    
    for sub in subs:
        text = sub.text.replace("\n", " ")  # Remove line breaks
        start_time = sub.start.ordinal / 1000
        end_time = sub.end.ordinal / 1000

        img = create_subtitle_image(text)
        img.save(temp_img_path)

        subtitle_clip = (ImageClip(temp_img_path, duration=end_time - start_time)
                         .set_position(("center", "center"))
                         .set_start(start_time))
        subtitle_clips.append(subtitle_clip)

    # Overlay subtitles onto the video
    final_video = CompositeVideoClip([video] + subtitle_clips)

    # Determine output file path
    if temp:
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
        output_path = temp_file.name
        temp_file.close()
    else:
        output_path = output_video_path

    # Save the final video
    final_video.write_videofile(output_path, codec="libx264", fps=fps, threads=os.cpu_count())

    print(f"Video with subtitles saved as {output_path}")
    
    return output_path

# Example usage
if __name__ == "__main__":
    output_video = add_subtitles_to_video("sample_video.mp4", "output.srt", "final_video.mp4", temp=False)
    print(f"Generated video path: {output_video}")

