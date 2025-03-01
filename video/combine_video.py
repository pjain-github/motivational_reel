from video import add_audio, add_music, add_subtitles

def combine_video(input_video_path, audio_path, subtitle_path, music_path):

    step1 = add_subtitles.add_subtitles_to_video(video_path=input_video_path, subtitle_path=subtitle_path)

    step2 = add_audio.add_audio_to_video(video_path=step1, audio_path=audio_path)

    step3 = add_music.add_background_music(video_path=step2, music_path=music_path, temp=True)

    return step3