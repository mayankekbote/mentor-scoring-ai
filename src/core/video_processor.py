"""
Video Processor Module
Handles video preprocessing: audio extraction and frame sampling.
"""

import os
import cv2
import ffmpeg
import numpy as np
from typing import List, Tuple
from src import config


class VideoProcessor:
    """
    Preprocesses video files for analysis.
    Extracts audio and samples frames at configurable intervals.
    """
    
    def __init__(self, video_path: str):
        """
        Initialize video processor.
        
        Args:
            video_path: Path to the input video file
        """
        self.video_path = video_path
        self.video_name = os.path.splitext(os.path.basename(video_path))[0]
        
    def extract_audio(self) -> str:
        """
        Extract audio from video using ffmpeg.
        Converts to mono, 16kHz WAV format (required by faster-whisper).
        
        Returns:
            Path to extracted audio file
            
        Raises:
            Exception: If ffmpeg extraction fails
        """
        audio_path = os.path.join(
            config.TEMP_DIR, 
            f"{self.video_name}_audio.wav"
        )
        
        try:
            # Use ffmpeg-python to extract audio
            # -ac 1: mono channel
            # -ar 16000: 16kHz sample rate
            # -y: overwrite output file
            (
                ffmpeg
                .input(self.video_path)
                .output(
                    audio_path,
                    ac=config.AUDIO_CHANNELS,
                    ar=config.AUDIO_SAMPLE_RATE,
                    format='wav'
                )
                .overwrite_output()
                .run(quiet=True, capture_stdout=True, capture_stderr=True)
            )
            
            return audio_path
            
        except ffmpeg.Error as e:
            error_msg = e.stderr.decode() if e.stderr else str(e)
            raise Exception(f"Audio extraction failed: {error_msg}")
    
    def sample_frames(self) -> Tuple[List[np.ndarray], float]:
        """
        Sample frames from video at regular intervals.
        
        Strategy:
        - Sample 1 frame every FRAME_SAMPLE_INTERVAL seconds
        - Limit to MAX_FRAMES_PER_MINUTE to prevent MediaPipe overload
        - This reduces processing time significantly for long videos
        
        Returns:
            Tuple of (list of sampled frames as numpy arrays, video duration in seconds)
            
        Raises:
            Exception: If video cannot be opened
        """
        cap = cv2.VideoCapture(self.video_path)
        
        if not cap.isOpened():
            raise Exception(f"Cannot open video file: {self.video_path}")
        
        # Get video properties
        fps = cap.get(cv2.CAP_PROP_FPS)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        duration = total_frames / fps if fps > 0 else 0
        
        # Calculate sampling strategy
        frame_interval = int(fps * config.FRAME_SAMPLE_INTERVAL)
        max_frames = int((duration / 60) * config.MAX_FRAMES_PER_MINUTE)
        
        sampled_frames = []
        frame_count = 0
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            # Sample frame at intervals
            if frame_count % frame_interval == 0:
                # Convert BGR to RGB (MediaPipe expects RGB)
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                sampled_frames.append(frame_rgb)
                
                # Stop if we've reached max frames
                if len(sampled_frames) >= max_frames:
                    break
            
            frame_count += 1
        
        cap.release()
        
        return sampled_frames, duration
    
    def get_video_duration(self) -> float:
        """
        Get video duration in seconds without processing frames.
        
        Returns:
            Duration in seconds
        """
        cap = cv2.VideoCapture(self.video_path)
        
        if not cap.isOpened():
            raise Exception(f"Cannot open video file: {self.video_path}")
        
        fps = cap.get(cv2.CAP_PROP_FPS)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        duration = total_frames / fps if fps > 0 else 0
        
        cap.release()
        
        return duration
    
    def cleanup(self):
        """
        Clean up temporary files created during processing.
        """
        audio_path = os.path.join(
            config.TEMP_DIR, 
            f"{self.video_name}_audio.wav"
        )
        
        if os.path.exists(audio_path):
            try:
                os.remove(audio_path)
            except Exception as e:
                print(f"Warning: Could not remove temporary audio file: {e}")


def process_video(video_path: str) -> Tuple[str, List[np.ndarray], float]:
    """
    Convenience function to process a video file.
    
    Args:
        video_path: Path to video file
        
    Returns:
        Tuple of (audio_path, sampled_frames, duration)
    """
    processor = VideoProcessor(video_path)
    audio_path = processor.extract_audio()
    frames, duration = processor.sample_frames()
    
    return audio_path, frames, duration
