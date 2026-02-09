"""
Speech-to-Text Module
Uses OpenAI Whisper API for fast transcription.
"""

from openai import OpenAI
from typing import List, Dict, Optional
import os
from src import config

# Global OpenAI client (lazy loading)
_openai_client: Optional[OpenAI] = None


def get_openai_client() -> OpenAI:
    """
    Get or initialize the OpenAI client (lazy loading).
    
    Returns:
        OpenAI client instance
        
    Raises:
        ValueError: If OPENAI_API_KEY is not set
    """
    global _openai_client
    
    if _openai_client is None:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError(
                "OPENAI_API_KEY environment variable not set. "
                "Please set it with: set OPENAI_API_KEY=your-key-here"
            )
        
        _openai_client = OpenAI(api_key=api_key)
        print("OpenAI client initialized")
    
    return _openai_client


class SpeechToText:
    """
    Transcribes audio using OpenAI Whisper API.
    Much faster than CPU-based faster-whisper.
    """
    
    def __init__(self):
        """Initialize speech-to-text processor."""
        self.client = None
    
    def transcribe_audio(self, audio_path: str, language: Optional[str] = None) -> List[Dict]:
        """
        Transcribe audio file to text using OpenAI Whisper API.
        
        Args:
            audio_path: Path to audio file (WAV, MP3, etc.)
            language: Language code (None for auto-detect, 'hi' for Hindi)
            
        Returns:
            List with single segment dictionary containing full transcript
        """
        # Lazy load client
        if self.client is None:
            self.client = get_openai_client()
        
        # Open audio file
        with open(audio_path, 'rb') as audio_file:
            # Call OpenAI Whisper API
            transcript = self.client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                language=language,  # None for auto-detect
                response_format="text"
            )
        
        # Return in same format as faster-whisper for compatibility
        return [{
            'text': transcript,
            'start': 0,
            'end': 0  # OpenAI doesn't provide timestamps in text mode
        }]
    
    def get_full_transcript(self, audio_path: str, language: Optional[str] = None) -> str:
        """
        Get full transcript as a single string.
        
        Args:
            audio_path: Path to audio file
            language: Language code (None for auto-detect)
            
        Returns:
            Full transcript text
        """
        segments = self.transcribe_audio(audio_path, language)
        return segments[0]['text']


def transcribe(audio_path: str, language: Optional[str] = None) -> str:
    """
    Convenience function to transcribe audio.
    
    Args:
        audio_path: Path to audio file
        language: Language code (None for auto-detect)
        
    Returns:
        Full transcript text
    """
    stt = SpeechToText()
    return stt.get_full_transcript(audio_path, language)


def transcribe_with_timestamps(audio_path: str, language: Optional[str] = None) -> List[Dict]:
    """
    Convenience function to transcribe with timestamps.
    
    Note: OpenAI Whisper API in text mode doesn't provide timestamps.
    For compatibility, returns single segment.
    
    Args:
        audio_path: Path to audio file
        language: Language code
        
    Returns:
        List of segments with text
    """
    stt = SpeechToText()
    return stt.transcribe_audio(audio_path, language)

