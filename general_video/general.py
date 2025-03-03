import asyncio
from moviepy.editor import AudioFileClip
from video.combine_video import combine_video
from video.test_subtitles import test_subtitles


class GeneralVideo:

    def __init__(self, llm_class, audio_class, pexels_class):
        self.llm = llm_class
        self.audio = audio_class
        self.pexels = pexels_class

    def pull_video(self, url: str=None):
        input_video, _ = self.pexels.download_video(link=url)

        return input_video
    
    def generate_audio(self, quote: str = None, rate: str = "-15%", pitch: str = "-15Hz"):
        # Generate auido from text
        audio_path = asyncio.run(self.audio.text_to_speech_edge(text=quote, rate=rate, pitch=pitch))

        return audio_path
    
    def test_subtitles(self, quote: str=None, audio_path: str=None, words_per_sec: int=2):

        subtitle_path = self.audio.generate_sub(mp3_file=audio_path)
        video_path = test_subtitles(audio_path=audio_path, subtitle_path=subtitle_path)

        return video_path, subtitle_path
    
    def generate_video(self, audio_path: str=None, video_path: str=None, music:str = "samples/sample_background_music.mp3"):

        subtitle_path = self.audio.generate_sub(mp3_file=audio_path)

        final_path = combine_video(input_video_path=video_path, audio_path=audio_path, subtitle_path=subtitle_path, music_path=music)

        return final_path







