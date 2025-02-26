import logging
import base64
import asyncio
from video.combine_video import combine_video


class LifestyleVideo:

    def __init__(self, llm_class, audio_class, pexels_class):
        self.llm = llm_class
        self.audio = audio_class
        self.pexels = pexels_class
        self.prompt = """
        Generate a motivational quote related to lifestyle and success, emphasizing the importance of a strong mindset in creating wealth. 
        The quote should be concise, impactful, and suitable for an Instagram Reel. 
        Since the quote will be converted into audio, ensure it is around {seconds} seconds long."""

    def generate_text(self, sec=15):

        prompt = self.prompt.format(
            seconds=str(sec)
        )
        text = self.llm.call_llm(prompt)
        logging.info({"Text generated": text})

        return text.content
    
    def pull_video(self, url: str=None):
        if url:
            input_video = self.pexels.download_video(link=url)

        else:
            input_video = None

        return input_video
    
    def verify_video(self, video_path: str, text: str):

        try:
            # 1. Encode the video to base64
            with open(video_path, "rb") as video_file:
                encoded_video = base64.b64encode(video_file.read()).decode("utf-8")

            # 2. Construct the message for the Gemini model, including the video data
            messages = [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "Describe this video."},  # Instruction
                        {"type": "video", "raw_bytes": encoded_video}
                    ]
                }
            ]

            # 3. Call the Gemini model
            response = self.call_llm(messages)  # Use your existing call_llm method

            # 4. Extract and return the description
            return response.content

        except Exception as e:
            logging.error(f"Error describing video: {e}")
            return None


    def generate_video(self, quote: str=None, url: str=None, music:str = "samples/sample_background_music.mp3"):

        video_path, time = self.pull_video(url)

        if not quote:
            quote = self.generate_text(time)

        audio_path = asyncio.run(self.audio.text_to_speech_edge(quote))

        subtitle_path = self.audio.generate_sub(quote)

        final_path = combine_video(input_video_path=video_path, audio_path=audio_path, subtitle_path=subtitle_path, music_path=music)

        return final_path







