from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.tools import Tool
import logging
import base64

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(filename)s - %(message)s'
)


class Gemini:
    """
    A class to interact with the Gemini model using Google Generative AI services.

    Attributes:
        api_key (str): The API key required to access the Gemini model.
        model (str): The specific model used, default is "models/gemini-1.5-flash".
        llm (ChatGoogleGenerativeAI): An instance of the ChatGoogleGenerativeAI model.

    Methods:
        stream_llm(messages: list, stream: bool = False) -> generator:
            Streams the response from the LLM in chunks if streaming is enabled.

        call_llm(messages: list, stream: bool = False) -> str:
            Invokes the LLM with the given messages and returns the full response.
    """

    def __init__(self, api_key, model="models/gemini-1.5-flash"):
        """
        Initializes the Gemini class with an API key and model, and sets up the LLM instance.

        Args:
            api_key (str): Your API key for accessing the Gemini model.
            model (str): The model identifier, default is "models/gemini-1.5-flash".
        """
        self.model = model
        self.api_key = api_key

        # Initialize the ChatGoogleGenerativeAI with specified parameters
        self.llm = ChatGoogleGenerativeAI(
            model=self.model,
            api_key=self.api_key,
            temperature=0,         # Controls the creativity of the response
            max_tokens=None,       # No limit on the number of tokens in the response
            timeout=None,          # No timeout is set for the response
            max_retries=2,         # Number of retries in case of failure
            # Other optional parameters can be added here...
        )

    def call_llm(self, messages, stream=False):
        """
        Invokes the LLM with the given messages and returns the full response.

        Args:
            messages (list): A list of messages to be sent to the LLM.
            stream (bool): If True, streaming is enabled, but it is not used in this function.

        Returns:
            str: The full response content from the LLM.
        """

        logging.info("Caling LLM...........................")
        response = self.llm.invoke(messages)
        logging.info("Response Genereted from LLM")

        return response
    
    def call_llm_json(self, messages, structure):
        """
        Invokes the LLM with the given messages and returns the full response in a structured format.
        """

        logging.info("Caling LLM...........................")
        structured_llm = self.llm.with_structured_output(structure)
        response = structured_llm.invoke(messages)
        logging.info("Response Genereted from LLM in strcutured json format")
        
        return response
    
    def describe_video(self, video_path):
        """
        Analyzes a video and generates a description using the Gemini model.

        Args:
            video_path (str): The path to the video file.

        Returns:
            str: The generated video description, or None if an error occurs.
        """
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

    def __str__(self):
        """
        Returns a string representation of the Gemini instance.
    
        Returns:
            str: A string describing the Gemini instance.
        """
        return f"Gemini(model={self.model}, api_key={'*' * len(self.api_key)})"
    
    def __repr__(self):
        """
        Returns a detailed string representation of the Gemini instance.
    
        Returns:
            str: A detailed string describing the Gemini instance.
        """
        return f"Gemini(model={self.model}, api_key={'*' * len(self.api_key)})"
        