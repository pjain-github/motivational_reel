from ai.gemini_util import Gemini
from ai.audio_util import Audio
from data_util.pexels_util import Pexels
from general_video.general import GeneralVideo
from dotenv import load_dotenv
import os

load_dotenv()

# Get the API key and CSE ID from environment variables
# google_api_key = os.getenv('GOOGLE_API_KEY')
# google_cse_id = os.getenv('GOOGLE_SEARCH_CSE_ID')
gemini_api_key = os.getenv('GOOGLE_API_KEY')
pexels_api_key = os.getenv('PEXELS_API_KEY')

def main(quote: str, video_url:str):

    llm = Gemini(api_key=gemini_api_key)
    audio = Audio()
    px = Pexels(pexels_api_key=pexels_api_key)

    gv = GeneralVideo(llm, audio, px)

    video_path = gv.generate_video(quote=quote, 
                      url=video_url, 
                      music="samples/sample_background_music.mp3")
    
    return video_path



if __name__=='__main__':
    main(
        quote="Wealth isn't built by chance, it's built by choice.  A powerful mindset is your most valuable asset.  Choose to believe, choose to act, choose to thrive.", 
        video_url="https://videos.pexels.com/video-files/7884420/7884420-sd_506_960_25fps.mp4")
    
