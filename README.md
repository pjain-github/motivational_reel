# Reel Generator

This Python application automatically generates short video reels based on a provided theme or random quote. It leverages various technologies like Gemini, Pexels, GTT (Google Text-to-Speech), Edge TTS, LangChain, PIL (Pillow), and MoviePy to create engaging video content.

## Features

* **Theme-based Reel Generation:**  Enter a theme (e.g., "motivational," "travel," "cooking") and the application will generate a reel with relevant visuals, text, and music.
* **Quote-based Reel Generation:** Provide a quote, and the application will create a reel incorporating the quote text and suitable background elements.
* **Automated Content Creation:**  The entire process of image/video selection, text-to-speech conversion, video editing, and audio integration is automated.
* **Customizable:**  The application can be further customized by modifying the code to use different video sources, fonts, music, or editing styles.

## Technologies Used

* **Gemini:** For generating creative text content and potentially assisting with theme selection.
* **Pexels:** For sourcing royalty-free stock videos and images.
* **GTT (Google Text-to-Speech) / Edge TTS:** For converting text to speech for the generated reels.  Edge TTS is preferred for higher quality if available.
* **LangChain:** For potentially managing prompts and chains related to text generation.
* **PIL (Pillow):** For image processing and manipulation.
* **MoviePy:** For video editing, combining video clips, adding text overlays, and audio integration.

## Project Structure

```
C:.
├── .env                  # Environment variables file
├── main.py               # Main application script
├── README.md             # This file
├── requirements.txt      # Project dependencies
├── ai                    # AI-related utilities
│   ├── audio_util.py     # Audio processing functions
│   ├── gemini_util.py    # Gemini API interaction
│   └── __pycache__       # Compiled Python files (can be ignored)
├── categories            # Predefined themes/categories
│   ├── children_stories.py
│   ├── health.py
│   ├── lifestyle.py
│   ├── lust.py        # Example - consider appropriate naming
│   ├── motivation.py
│   └── __init__.py
├── data                  # Data handling utilities
│   ├── pexels_util.py    # Pexels API interaction
│   └── __init__.py
├── fonts                 # Font files
│   ├── __init__.py
│   └── freesans-font     # Example font directory
│       ├── ...           # Font files (.otf, .ttf)
│       └── misc          # Font metadata
├── samples               # Sample input/output files
│   ├── input_video.mp4   # Example input video
│   ├── sample_background_music.mp3 # Example background music
│   ├── subtitles.mp4    # Example subtitles
│   └── video_with_music.mp4 # Example output video
└── video                 # Video processing functions
    ├── add_audio.py      # Add audio to video
    ├── add_music.py      # Add background music
    ├── add_subtitles.py  # Add subtitles to video
    ├── combine_video.py  # Combine video clips
    ├── generate_subtitle.py # Generate subtitles from text
    └── __init__.py
```

## Setup and Installation

1. **Clone the Repository:** (If applicable)

   ```bash
   git clone <repository_url>
   ```

2. **Create a Virtual Environment:** (Recommended)

   ```bash
   python3 -m venv .venv  # Create a virtual environment
   source .venv/bin/activate  # Activate the environment (Linux/macOS)
   .venv\Scripts\activate  # Activate the environment (Windows)
   ```

3. **Install Dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Variables (.env):**

   Create a `.env` file in the project root directory and add the following environment variables:

   ```
   GEMINI_API_KEY=<your_gemini_api_key>
   PEXELS_API_KEY=<your_pexels_api_key>
   # Optionally, if using Edge TTS:
   EDGE_TTS_PATH=<path_to_edge_tts_executable> # Example: C:\path\to\msedge-tts.exe
   # Add any other required environment variables.
   ```

   * **Gemini API Key:** Obtain your Gemini API key from Google Cloud Platform.
   * **Pexels API Key:** Get your Pexels API key from the Pexels developer website.
   * **Edge TTS Path:**  If you want to use Edge TTS (recommended), download the Microsoft Edge Text-to-Speech command-line tool and provide the path to the executable. If you want to use GTT, you don't need this.
   * **GTT:** No API key is needed for GTT.

5. **Font Files:**

   Place your desired font files (e.g., `.ttf`, `.otf`) in the `fonts/freesans-font` directory or create your own font directory and update the code accordingly.

6. **Sample Files:**

   The `samples` directory contains example input video, music, and output video files. You can replace these with your own files.

## Usage

1. **Run the Main Script:**

   ```bash
   python main.py
   ```

2. **Input:**

   The `main.py` script will likely prompt you to enter a theme or a quote.

3. **Output:**

   The generated reel will be saved in a specified output directory (you'll likely need to configure this in the script).

## Further Development

* **More Themes/Categories:** Add more predefined themes or categories to expand the application's capabilities.
* **Customization Options:** Allow users to customize various parameters, such as video length, music choice, font selection, and transition effects.
* **User Interface:** Develop a graphical user interface (GUI) for easier interaction.
* **Error Handling:** Implement robust error handling to handle API request failures, file processing issues, and other potential problems.

## Contributing

(Add contribution guidelines if you plan to open-source the project)
```

Remember to replace the placeholder values (e.g., `<your_api_key>`, `<repository_url>`) with your actual keys and repository information.  Also, adapt the `Usage` section to reflect the actual input method used by your `main.py` script.  This detailed README should provide a good starting point for anyone looking to understand and use your Reel Generator application.
