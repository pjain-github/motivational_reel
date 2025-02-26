import tempfile
from moviepy.editor import ImageClip, concatenate_videoclips, ColorClip
from PIL import Image, ImageDraw, ImageFont
import pysrt
import os

def generate_subtitle_video(
        subtitle_path: str, 
        output_subtitle_video: str = "samples/subtitles.mp4", 
        font_path: str = "fonts/freesans-font/FreeSans-LrmZ.ttf",
        temp: bool = True,
        video_width: int = 1920,
        video_height: int = 1080
    ) -> str:
    """
    Generates a video with subtitles on a blank black background.
    
    :param subtitle_path: Path to the subtitle (.srt) file
    :param output_subtitle_video: Path to save the output video
    :param font_path: Path to the font file (optional)
    :param temp: If True, saves the video in a temporary file
    :param video_width: Width of subtitle video file
    :param video_height: Height of subtitle video file
    :return: Path of the saved video file
    """
    # Video properties
    fps = 30  # Frames per second

    # Load subtitles
    subs = pysrt.open(subtitle_path)

    # Function to create subtitle images
    def create_subtitle_image(text):
        """Creates an image with subtitles centered."""
        img = Image.new("RGBA", (video_width, video_height), (0, 0, 0, 0))  # Transparent background
        draw = ImageDraw.Draw(img)

        font_size = video_height/20
        # Load font (use default if not provided)
        try:
            font = ImageFont.truetype(font_path, size=font_size) if font_path else ImageFont.load_default()
        except:
            font = ImageFont.load_default()

        # Text size
        text_w, text_h = draw.textbbox((0, 0), text, font=font)[2:]

        # Position text at the center
        x = (video_width - text_w) // 2
        y = (video_height - text_h) // 2

        # Draw gray background rectangle
        draw.rectangle([x - 5, y - 3, x + text_w + 5, y + text_h + 3], fill="grey")

        # Draw white text
        draw.text((x, y), text, font=font, fill="white")

        return img

    # Create subtitle clips
    subtitle_clips = []
    for sub in subs:
        text = sub.text.replace("\n", " ")  # Remove line breaks
        start_time = sub.start.ordinal / 1000
        end_time = sub.end.ordinal / 1000

        img = create_subtitle_image(text)
        img.save("temp_subtitle.png")

        subtitle_clip = ImageClip("temp_subtitle.png", duration=end_time - start_time).set_position(("center", "center"))
        subtitle_clips.append(subtitle_clip.set_start(start_time))

    # Create a blank video with black background
    video_duration = subs[-1].end.ordinal / 1000  # Duration based on last subtitle
    video = ColorClip(size=(video_width, video_height), color=(0, 0, 0), duration=video_duration)

    # Overlay subtitles onto the blank video
    final_video = concatenate_videoclips(subtitle_clips, method="compose")

    # Determine output file path
    if temp:
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
        output_path = temp_file.name
        temp_file.close()
    else:
        output_path = output_subtitle_video

    # Save the subtitle-only video
    final_video.write_videofile(output_path, codec="libx264", fps=fps)

    print(f"Subtitle video saved as {output_path}")
    
    return output_path  # Return the file path of the saved video

# Example usage
if __name__=="__main__":
    video_path = generate_subtitle_video("output.srt", "subtitles.mp4", temp=False)
    print(f"Generated video path: {video_path}")
