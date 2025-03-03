import cv2
import numpy as np
from moviepy.editor import VideoFileClip, ImageSequenceClip
import tempfile

def convert_image_to_video(image_path, time=5, output_path="samples/image_to_video.mp4", fps=30, zoom_factor=1.5, temp=True):
    # Load the image
    image = cv2.imread(image_path)
    height, width, _ = image.shape
    
    # Calculate zoom steps
    total_frames = time * fps
    zoomed_images = []
    
    for i in range(total_frames):
        scale = 1 + (zoom_factor - 1) * (i / total_frames)  # Gradually increase scale
        new_width = int(width / scale)
        new_height = int(height / scale)
        
        x_start = (width - new_width) // 2
        y_start = (height - new_height) // 2
        
        cropped = image[y_start:y_start + new_height, x_start:x_start + new_width]
        resized = cv2.resize(cropped, (width, height), interpolation=cv2.INTER_LINEAR)
        zoomed_images.append(resized[:, :, ::-1])  # Convert BGR to RGB for MoviePy
    
    # Create video from images
    clip = ImageSequenceClip(zoomed_images, fps=fps)

    if temp:
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
        output_path = temp_file.name
        temp_file.close()

    clip.write_videofile(output_path, codec="libx264")
    
    print(f"Video saved at {output_path}")
    return output_path

# Example usage
# convert_image_to_video("input.jpg", 5, "zoom_video.mp4")
