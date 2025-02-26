from gtts import gTTS
import pysrt
import asyncio
import edge_tts
import tempfile


class Audio:

    def __init__(self):
        pass

    def seconds_to_srt_time(self, seconds):
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        milliseconds = int((seconds - int(seconds)) * 1000)
        return pysrt.SubRipTime(hours, minutes, secs, milliseconds)

    def generate_sub(self, text: str, subtitle_filename: str = "samples/subtitle.srt", temp: bool=True):
        subs = []
        words = text.split()
        start_time = 0.0
        words_per_second = 2.3  # Approximate speech speed

        frame = []
        for word in words:
            if sum(len(w) for w in frame) + len(frame) + len(word) <= 12:
                frame.append(word)
            else:
                # Save the current frame as a subtitle
                end_time = start_time + (len(frame) / words_per_second)
                subs.append(pysrt.SubRipItem(
                    index=len(subs) + 1,
                    start=self.seconds_to_srt_time(start_time),
                    end=self.seconds_to_srt_time(end_time),
                    text=" ".join(frame)
                ))
                start_time = end_time  # Update start time
                frame = [word]  # Start new frame


        # Add last frame if not empty
        if frame:
            end_time = start_time + (len(frame) / words_per_second)
            subs.append(pysrt.SubRipItem(
                index=len(subs) + 1,
                start=self.seconds_to_srt_time(start_time),
                end=self.seconds_to_srt_time(end_time),
                text=" ".join(frame)
            ))

        # Save subtitle file
        subs_file = pysrt.SubRipFile(items=subs)

        if temp:
            temp_file = tempfile.NamedTemporaryFile(suffix=".srt", delete=False)
            subtitle_filename = temp_file.name

        subs_file.save(subtitle_filename, encoding="utf-8")
        print(f"Subtitles saved as {subtitle_filename}")

        return subtitle_filename
    
    def female_audio(self, text:str, audio_filename="samples/audio.mp3", temp: bool=True):
        # Convert text to speech
        tts = gTTS(text)

        if temp:
            temp_file = tempfile.NamedTemporaryFile(suffix=".mp3", delete=False)
            audio_filename = temp_file.name
        
        tts.save(audio_filename)

        return audio_filename
    
    async def text_to_speech_edge(self, text: str, audio_filename="samples/audio.mp3", temp: bool=True):
        voice = "en-US-ChristopherNeural"  # Choose a male voice (e.g., Guy, Eric, Roger)
        tts = edge_tts.Communicate(text, voice)

        if temp:
            temp_file = tempfile.NamedTemporaryFile(suffix=".mp3", delete=False)
            audio_filename = temp_file.name

        await tts.save(audio_filename)
        print(f"Audio saved as {audio_filename}")

        return audio_filename
    

