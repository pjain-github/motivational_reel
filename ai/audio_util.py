from gtts import gTTS
import pysrt
import asyncio
import edge_tts
import tempfile
import whisper
import textwrap


class Audio:

    def __init__(self):
        pass

    def seconds_to_srt_time(self, seconds):
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        milliseconds = int((seconds - int(seconds)) * 1000)
        return pysrt.SubRipTime(hours, minutes, secs, milliseconds)
    
    def format_time(self, seconds):
        """Convert time in seconds to SRT format (hh:mm:ss,ms)"""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        millis = int((seconds % 1) * 1000)
        return f"{hours:02}:{minutes:02}:{secs:02},{millis:03}"
    
    def generate_sub(self, mp3_file: str="samples/audio.mp3", subtitle_filename: str = "samples/subtitle.srt", temp: bool=True):
        # Load the Whisper Tiny model
        model = whisper.load_model("tiny")

        # Transcribe the audio
        result = model.transcribe(mp3_file)

        # Save the subtitles to a file
        if temp:
            temp_file = tempfile.NamedTemporaryFile(suffix=".srt", delete=False)
            subtitle_filename = temp_file.name

        with open(subtitle_filename, "w", encoding="utf-8") as f:
            index = 1
            for segment in result["segments"]:
                start_time = segment["start"]
                end_time = segment["end"]
                text = segment["text"]

                # Split the text into chunks of max 15 characters
                text_chunks = textwrap.wrap(text, width=15)

                chunk_duration = (end_time - start_time) / max(len(text_chunks), 1)  # Duration per chunk

                for i, chunk in enumerate(text_chunks):
                    chunk_start = start_time + (i * chunk_duration)
                    chunk_end = chunk_start + chunk_duration

                    f.write(f"{index}\n")
                    f.write(f"{self.format_time(chunk_start)} --> {self.format_time(chunk_end)}\n")
                    f.write(f"{chunk}\n\n")
                    index += 1

        print(f"Subtitles saved as: {subtitle_filename}")
        return subtitle_filename

    # def generate_sub(self, text: str, words_per_sec: int=2.3, subtitle_filename: str = "samples/subtitle.srt", temp: bool=True):
    #     subs = []
    #     words = text.split()
    #     start_time = 0.0
    #     words_per_second = words_per_sec  # Approximate speech speed

    #     frame = []
    #     for word in words:
    #         if sum(len(w) for w in frame) + len(frame) + len(word) <= 12:
    #             frame.append(word)
    #         else:
    #             # Save the current frame as a subtitle
    #             end_time = start_time + (len(frame) / words_per_second)
    #             subs.append(pysrt.SubRipItem(
    #                 index=len(subs) + 1,
    #                 start=self.seconds_to_srt_time(start_time),
    #                 end=self.seconds_to_srt_time(end_time),
    #                 text=" ".join(frame)
    #             ))
    #             start_time = end_time  # Update start time
    #             frame = [word]  # Start new frame


    #     # Add last frame if not empty
    #     if frame:
    #         end_time = start_time + (len(frame) / words_per_second)
    #         subs.append(pysrt.SubRipItem(
    #             index=len(subs) + 1,
    #             start=self.seconds_to_srt_time(start_time),
    #             end=self.seconds_to_srt_time(end_time),
    #             text=" ".join(frame)
    #         ))

    #     # Save subtitle file
    #     subs_file = pysrt.SubRipFile(items=subs)

    #     if temp:
    #         temp_file = tempfile.NamedTemporaryFile(suffix=".srt", delete=False)
    #         subtitle_filename = temp_file.name

    #     subs_file.save(subtitle_filename, encoding="utf-8")
    #     print(f"Subtitles saved as {subtitle_filename}")

    #     return subtitle_filename
    
    def female_audio(self, text:str, audio_filename="samples/audio.mp3", temp: bool=True):
        # Convert text to speech
        tts = gTTS(text)

        if temp:
            temp_file = tempfile.NamedTemporaryFile(suffix=".mp3", delete=False)
            audio_filename = temp_file.name
        
        tts.save(audio_filename)

        return audio_filename
    
    async def text_to_speech_edge(self, text: str, audio_filename: str="samples/audio.mp3", rate: str="-2%", pitch: str="-1Hz", temp: bool=True):
        voice = "en-US-ChristopherNeural"  # Choose a male voice (e.g., Guy, Eric, Roger)

        if pitch and rate:
            tts = edge_tts.Communicate(text, voice=voice, rate=rate, pitch=pitch)
        elif pitch:
            tts = edge_tts.Communicate(text, voice=voice, pitch=pitch)
        elif rate:
            tts = edge_tts.Communicate(text, voice=voice, rate=rate)
        else:
            tts = edge_tts.Communicate(text, voice=voice)

        if temp:
            temp_file = tempfile.NamedTemporaryFile(suffix=".mp3", delete=False)
            audio_filename = temp_file.name
            temp_file = tempfile.NamedTemporaryFile(suffix=".srt", delete=False)
            subtile_filename = temp_file.name

        await tts.save(audio_filename)
        print(f"Audio saved as {audio_filename}")

        return audio_filename
    
if __name__=="__main__":
    audio = Audio()
    asyncio.run(audio.text_to_speech_edge(text="Ever heard a success story that starts with quitting? NO! Because winners don’t give up. They fight, they push, they keep going. Be that person. KEEP GOING!", rate="-20%", pitch="-17Hz", temp=False))
    
    

