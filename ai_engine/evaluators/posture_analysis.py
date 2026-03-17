"""
Posture Analysis Evaluator
Uses MediaPipe Pose to estimate body posture quality from video frames.

Input:  list of RGB numpy arrays (sampled video frames)
Output: dict with alignment metrics and a 0-100 score
"""

import mediapipe as mp
import numpy as np
from typing import Dict, List

mp_pose = mp.solutions.pose


def analyze_posture(frames: List[np.ndarray]) -> Dict:
    """
    Analyze body posture across a list of RGB video frames.

    Args:
        frames: List of H×W×3 uint8 numpy arrays in RGB color space.
                Typically sampled at regular intervals from a video.

    Returns:
        Dictionary with keys:
            - ``frames_analyzed``   (int):   Number of frames where a pose was detected.
            - ``frames_total``      (int):   Total frames passed in.
            - ``detection_rate``    (float): Fraction of frames with pose detected.
            - ``score``             (float): 0-100 posture quality score.
    """
    if not frames:
        return {"frames_analyzed": 0, "frames_total": 0, "detection_rate": 0.0, "score": 20.0}

    scores: List[float] = []
    confidences: List[float] = []

    with mp_pose.Pose(
        static_image_mode=True,
        model_complexity=1,
        enable_segmentation=False,
        smooth_landmarks=False,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5,
    ) as pose:
        for frame in frames:
            result = pose.process(frame)
            if not result.pose_landmarks:
                continue

            lm = result.pose_landmarks.landmark
            alignment, conf = _score_frame(lm)
            if conf > 0.5:
                scores.append(alignment)
                confidences.append(conf)

    if not scores:
        return {
            "frames_analyzed": 0,
            "frames_total": len(frames),
            "detection_rate": 0.0,
            "score": 20.0,
        }

    weighted_score = float(np.average(scores, weights=confidences))
    return {
        "frames_analyzed": len(scores),
        "frames_total": len(frames),
        "detection_rate": round(len(scores) / len(frames), 3),
        "score": round(min(100.0, max(0.0, weighted_score)), 1),
    }


# ── Private helpers ────────────────────────────────────────────────────────────

def _score_frame(landmarks) -> tuple:
    """
    Compute alignment score and confidence for a single frame.

    Returns:
        (alignment_score: float 0-100, confidence: float 0-1)
    """
    L_SH = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER]
    R_SH = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER]
    L_HI = landmarks[mp_pose.PoseLandmark.LEFT_HIP]
    R_HI = landmarks[mp_pose.PoseLandmark.RIGHT_HIP]

    # Midpoints
    sh_mid_x = (L_SH.x + R_SH.x) / 2
    hi_mid_x = (L_HI.x + R_HI.x) / 2

    # Lateral offset (shoulder should be above hip with small horizontal deviation)
    h_offset = abs(sh_mid_x - hi_mid_x)
    # Shoulder levelness
    sh_tilt = abs(L_SH.y - R_SH.y)
    # Hip levelness
    hi_tilt = abs(L_HI.y - R_HI.y)

    alignment = 100.0 * (1.0 - min(h_offset * 2, 1.0))
    sh_level = 100.0 * (1.0 - min(sh_tilt * 3, 1.0))
    hi_level = 100.0 * (1.0 - min(hi_tilt * 3, 1.0))

    score = 0.5 * alignment + 0.3 * sh_level + 0.2 * hi_level
    confidence = float(np.mean([L_SH.visibility, R_SH.visibility, L_HI.visibility, R_HI.visibility]))

    return max(0.0, min(100.0, score)), confidence
