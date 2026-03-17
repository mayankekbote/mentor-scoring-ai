"""
Whisper Client Module
Wraps OpenAI Whisper API for audio transcription.
Designed for easy replacement or extension (e.g., swap to local Whisper).
"""

import os
from dotenv import load_dotenv
from typing import Optional
from openai import OpenAI


# Lazy-loaded singleton client
_client: Optional[OpenAI] = None


def _get_client() -> OpenAI:
    """
    Return the cached OpenAI client, initializing it on first call.

    Raises:
        ValueError: If OPENAI_API_KEY is not set in environment.
    """
    global _client
    if _client is None:
        load_dotenv()
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError(
                "OPENAI_API_KEY environment variable is not set. "
                "Add it to your .env file or export it in your shell."
            )
        _client = OpenAI(api_key=api_key)
    return _client


class WhisperClient:
    """
    Client for OpenAI Whisper transcription API.

    Usage:
        client = WhisperClient()
        transcript = client.transcribe("path/to/audio.wav")
    """

    def __init__(self, model: str = "whisper-1"):
        """
        Args:
            model: Whisper model name (default: whisper-1).
        """
        self.model = model

    def transcribe(self, audio_path: str, language: Optional[str] = None) -> str:
        """
        Transcribe an audio file to text.

        Args:
            audio_path: Absolute or relative path to a WAV/MP3/MP4 audio file.
            language:   BCP-47 language code for forced decoding (e.g. 'en', 'hi').
                        Pass None for Whisper's automatic language detection.

        Returns:
            Transcribed text as a plain string.

        Raises:
            FileNotFoundError: If audio_path does not exist.
            ValueError: If the API key is missing.
        """
        if not os.path.exists(audio_path):
            raise FileNotFoundError(f"Audio file not found: {audio_path}")

        client = _get_client()

        with open(audio_path, "rb") as audio_file:
            response = client.audio.transcriptions.create(
                model=self.model,
                file=audio_file,
                language=language,
                response_format="text",
            )

        # OpenAI SDK returns a plain str when response_format="text"
        return str(response).strip()
