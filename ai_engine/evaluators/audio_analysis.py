"""
Audio Analysis Evaluator
Analyzes audio features (RMS energy) to compute an audio quality score.

Input:  path to a WAV audio file (mono, 16 kHz recommended)
Output: dict with numeric metrics and a 0-100 score
"""

import librosa
import numpy as np
from typing import Dict

# ── Audio feature thresholds (tuned for typical teaching scenarios) ────────────
_RMS_MIN = 0.01      # Very quiet
_RMS_OPTIMAL = 0.10  # Good volume
_RMS_MAX = 0.30      # Very loud
_SAMPLE_RATE = 16000  # Hz


def analyze_audio(audio_path: str) -> Dict:
    """
    Analyze audio quality from a WAV file.

    Args:
        audio_path: Path to an audio file supported by librosa.

    Returns:
        Dictionary with keys:
            - ``rms_energy`` (float): Mean RMS energy.
            - ``score``      (float): Audio quality score 0-100.
    """
    y, sr = librosa.load(audio_path, sr=_SAMPLE_RATE, mono=True)
    rms_energy = float(np.mean(librosa.feature.rms(y=y)[0]))
    score = _score_rms(rms_energy)
    return {
        "rms_energy": round(rms_energy, 6),
        "score": round(score, 1),
    }


# ── Private helpers ────────────────────────────────────────────────────────────

def _score_rms(energy: float) -> float:
    """Map RMS energy to a 0-100 score."""
    if energy < _RMS_MIN:
        return 40.0  # Too quiet
    if energy > _RMS_MAX:
        return 70.0  # Too loud (clipping risk)

    deviation = abs(energy - _RMS_OPTIMAL)
    max_deviation = _RMS_MAX - _RMS_OPTIMAL
    score = 100.0 * (1.0 - deviation / max_deviation)
    return max(70.0, min(100.0, score))
