"""
Audio Analyzer Module
Extracts audio features using librosa and computes audio quality score.
"""

import librosa
import numpy as np
from typing import Dict
from src import config


class AudioAnalyzer:
    """
    Analyzes audio features to evaluate voice quality.
    Extracts pitch variance, RMS energy, and speaking rate.
    """
    
    def __init__(self, audio_path: str):
        """
        Initialize audio analyzer.
        
        Args:
            audio_path: Path to audio file (WAV format, 16kHz mono)
        """
        self.audio_path = audio_path
        self.y = None
        self.sr = None
        
    def load_audio(self):
        """Load audio file using librosa."""
        if self.y is None:
            self.y, self.sr = librosa.load(
                self.audio_path, 
                sr=config.AUDIO_SAMPLE_RATE,
                mono=True
            )
    
    def extract_features(self) -> Dict[str, float]:
        """
        Extract audio features for scoring.
        
        SIMPLIFIED: Only extracts RMS energy for speed.
        
        Returns:
            Dictionary with:
            - rms_energy: Root mean square energy
        """
        self.load_audio()
        
        # Only RMS energy (volume/loudness) - fast and simple
        rms_energy = self._extract_rms_energy()
        
        return {
            'rms_energy': rms_energy
        }
    
    def _extract_rms_energy(self) -> float:
        """
        Extract RMS (root mean square) energy.
        
        Indicates volume/loudness of speech.
        
        Returns:
            Mean RMS energy
        """
        rms = librosa.feature.rms(y=self.y)[0]
        return float(np.mean(rms))
    
    def compute_score(self) -> float:
        """
        Compute overall audio quality score (0-100).
        
        SIMPLIFIED: Only uses RMS energy (volume).
        
        Returns:
            Audio quality score (0-100)
        """
        features = self.extract_features()
        
        # Score only RMS energy
        energy_score = self._score_rms_energy(features['rms_energy'])
        
        # Return energy score directly
        return max(0, min(100, energy_score))
    
    
    def _score_rms_energy(self, energy: float) -> float:
        """
        Score RMS energy on 0-100 scale.
        
        Optimal energy indicates good volume.
        Too low = hard to hear, too high = shouting.
        """
        if energy < config.RMS_ENERGY_MIN:
            # Too quiet
            return 40
        elif energy > config.RMS_ENERGY_MAX:
            # Too loud
            return 70
        else:
            # Score based on proximity to optimal
            deviation = abs(energy - config.RMS_ENERGY_OPTIMAL)
            max_deviation = config.RMS_ENERGY_MAX - config.RMS_ENERGY_OPTIMAL
            score = 100 * (1 - deviation / max_deviation)
            return max(70, score)


def analyze_audio(audio_path: str) -> float:
    """
    Convenience function to analyze audio and return score.
    
    Args:
        audio_path: Path to audio file
        
    Returns:
        Audio quality score (0-100)
    """
    analyzer = AudioAnalyzer(audio_path)
    return analyzer.compute_score()
