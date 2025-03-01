import requests
import logging
import tempfile
import os
import cv2

class Pexels:

    def __init__(self, pexels_api_key):
        self.api_key = pexels_api_key
        self.BASE_URL = "https://api.pexels.com/videos/search"
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    def get_pexels_videos(self, query: str, per_page: int = 10, page: int = 1):
        """Fetches Pexels videos based on the query."""
        headers = {"Authorization": self.api_key}
        params = {
            "query": query,
            "per_page": per_page,
            "page": page,
            "orientation": "portrait"  # Ensures vertical videos
        }
        
        try:
            response = requests.get(self.BASE_URL, headers=headers, params=params)
            response.raise_for_status()
            data = response.json()
            videos = data.get("videos", [])
            return videos
        except requests.exceptions.RequestException as e:
            logging.error(f"Failed to fetch videos: {e}")
            return []

    def download_video(self, link: str, output_path: str = "samples/input_video.mp4", temp: bool = True):
        """Downloads a video from the given link and saves it to output_path or a temporary file."""
        try:
            logging.info(f"Starting download: {link}")
            response = requests.get(link, stream=True)
            response.raise_for_status()
            
            if temp:
                temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
                output_path = temp_file.name
                logging.info(f"Using temporary file: {output_path}")
            
            with open(output_path, "wb") as file:
                for chunk in response.iter_content(chunk_size=1024 * 1024):  # 1MB chunks
                    file.write(chunk)
            
            logging.info(f"Download completed: {output_path}")

            # Get video duration
            cap = cv2.VideoCapture(output_path)
            fps = cap.get(cv2.CAP_PROP_FPS)
            frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)
            duration = frame_count / fps if fps > 0 else 0
            cap.release()
            
            logging.info(f"Video duration: {duration} seconds")
            return output_path, duration
        except requests.exceptions.RequestException as e:
            logging.error(f"Failed to download video: {e}")
            return None, None


