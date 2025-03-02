import whisper
import textwrap

def transcribe_audio(mp3_file):
    # Load the Whisper Tiny model
    model = whisper.load_model("tiny")
    
    # Transcribe the audio
    result = model.transcribe(mp3_file)
    
    # Save the subtitles to a file
    srt_file = mp3_file.replace(".mp3", ".srt")
    with open(srt_file, "w", encoding="utf-8") as f:
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
                f.write(f"{format_time(chunk_start)} --> {format_time(chunk_end)}\n")
                f.write(f"{chunk}\n\n")
                index += 1

    print(f"Subtitles saved as: {srt_file}")

def format_time(seconds):
    """Convert time in seconds to SRT format (hh:mm:ss,ms)"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int((seconds % 1) * 1000)
    return f"{hours:02}:{minutes:02}:{secs:02},{millis:03}"

# Example usage
transcribe_audio("audio.mp3")  # Replace with your MP3 file name
