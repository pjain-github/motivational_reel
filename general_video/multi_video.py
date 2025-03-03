import asyncio
from moviepy.editor import AudioFileClip
from video.combine_video import combine_video, merge_video
from video.test_subtitles import test_subtitles
from video.add_music import add_background_music
from video.image_to_video import convert_image_to_video


class MultiVideo:

    def __init__(self, llm_class, audio_class, pexels_class):
        self.llm = llm_class
        self.audio = audio_class
        self.pexels = pexels_class

    def pull_video(self, url: str=None):
        input_video, _ = self.pexels.download_video(link=url)

        return input_video
    
    def get_video_from_image(self, image_path: str=None, time:str=5):
        video_path = convert_image_to_video(image_path=image_path, time=time)
        return video_path
    
    def pull_image(self, url: str=None, time: int=5):
        input_image = self.pexels.download_image_pexels(link=url)
        video_path = self.get_video_from_image(input_image, time)

        return video_path

    def generate_audio(self, quote: str = None, rate: str = "-15%", pitch: str = "-15Hz"):
        # Generate auido from text
        audio_path = asyncio.run(self.audio.text_to_speech_edge(text=quote, rate=rate, pitch=pitch))

        return audio_path
    
    def test_subtitles(self, audio_path: str=None):

        subtitle_path = self.audio.generate_sub(mp3_file=audio_path)
        video_path = test_subtitles(audio_path=audio_path, subtitle_path=subtitle_path)

        return video_path, subtitle_path
    
    def generate_multi_video(self, data_list, music:str = "samples/sample_background_music.mp3"):

        videos = []

        print("*************")

        print(data_list)

        for data in data_list:

            audio_path = data["audio_path"]
            video_path = data["video_path"]
            subtitle_path =  self.audio.generate_sub(mp3_file=audio_path)

            video = combine_video(input_video_path=video_path, audio_path=audio_path, subtitle_path=subtitle_path)

            videos.append(video)

        video = merge_video(video_paths=videos)

        final_path = add_background_music(video_path=video, music_path=music)

        # final_path = combine_video(input_video_path=video_path, audio_path=audio_path, subtitle_path=subtitle_path, music_path=music)

        return final_path
    
    def generate_multi_video_simple(self, audio_path=None, video_paths: str=None, music:str = "samples/sample_background_music.mp3"):

        video_path = merge_video(video_paths=video_paths)
        subtitle_path = self.audio.generate_sub(mp3_file=audio_path)

        final_path = combine_video(input_video_path=video_path, audio_path=audio_path, subtitle_path=subtitle_path, music_path=music)

        return final_path







