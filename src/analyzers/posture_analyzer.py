"""
Posture Analyzer Module
Uses MediaPipe Pose to analyze body posture from video frames.
"""

import mediapipe as mp
import numpy as np
from typing import List, Dict
from src import config

# MediaPipe Pose solution (NOT mediapipe.tasks)
mp_pose = mp.solutions.pose


class PostureAnalyzer:
    """
    Analyzes body posture using MediaPipe Pose.
    Computes posture score based on shoulder-hip vertical alignment.
    """
    
    def __init__(self):
        """
        Initialize MediaPipe Pose with explicit parameters.
        
        Design choice: static_image_mode=True because we process
        individual sampled frames, not continuous video stream.
        """
        self.pose = mp_pose.Pose(
            static_image_mode=config.MEDIAPIPE_STATIC_IMAGE_MODE,
            model_complexity=1,  # 0=lite, 1=full, 2=heavy
            enable_segmentation=config.MEDIAPIPE_ENABLE_SEGMENTATION,
            smooth_landmarks=config.MEDIAPIPE_SMOOTH_LANDMARKS,
            min_detection_confidence=config.MEDIAPIPE_MIN_DETECTION_CONFIDENCE,
            min_tracking_confidence=config.MEDIAPIPE_MIN_TRACKING_CONFIDENCE
        )
    
    def analyze_frame(self, frame: np.ndarray) -> Dict[str, float]:
        """
        Analyze a single frame for posture.
        
        Args:
            frame: RGB image as numpy array
            
        Returns:
            Dictionary with posture metrics:
            - alignment_score: 0-100 (vertical alignment quality)
            - confidence: 0-1 (detection confidence)
            - detected: bool (whether pose was detected)
        """
        results = self.pose.process(frame)
        
        if not results.pose_landmarks:
            return {
                'alignment_score': 0,
                'confidence': 0,
                'detected': False
            }
        
        landmarks = results.pose_landmarks.landmark
        
        # Get key points for posture analysis
        # Using shoulder and hip landmarks
        left_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER]
        right_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER]
        left_hip = landmarks[mp_pose.PoseLandmark.LEFT_HIP]
        right_hip = landmarks[mp_pose.PoseLandmark.RIGHT_HIP]
        
        # Calculate alignment score
        alignment_score = self._calculate_alignment(
            left_shoulder, right_shoulder, left_hip, right_hip
        )
        
        # Average visibility as confidence
        confidence = np.mean([
            left_shoulder.visibility,
            right_shoulder.visibility,
            left_hip.visibility,
            right_hip.visibility
        ])
        
        return {
            'alignment_score': alignment_score,
            'confidence': confidence,
            'detected': True
        }
    
    def _calculate_alignment(self, left_shoulder, right_shoulder, 
                            left_hip, right_hip) -> float:
        """
        Calculate posture alignment score based on shoulder-hip vertical alignment.
        
        Good posture characteristics:
        - Shoulders roughly above hips (small horizontal offset)
        - Shoulders level (similar y-coordinates)
        - Hips level (similar y-coordinates)
        
        Args:
            left_shoulder, right_shoulder, left_hip, right_hip: MediaPipe landmarks
            
        Returns:
            Alignment score (0-100)
        """
        # Calculate midpoints
        shoulder_mid_x = (left_shoulder.x + right_shoulder.x) / 2
        shoulder_mid_y = (left_shoulder.y + right_shoulder.y) / 2
        hip_mid_x = (left_hip.x + right_hip.x) / 2
        hip_mid_y = (left_hip.y + right_hip.y) / 2
        
        # Vertical alignment: shoulders should be above hips with minimal horizontal offset
        horizontal_offset = abs(shoulder_mid_x - hip_mid_x)
        
        # Shoulder levelness
        shoulder_tilt = abs(left_shoulder.y - right_shoulder.y)
        
        # Hip levelness
        hip_tilt = abs(left_hip.y - right_hip.y)
        
        # Score calculation (inverse of deviations)
        # Lower offset/tilt = higher score
        alignment_score = 100 * (1 - min(horizontal_offset * 2, 1.0))
        shoulder_level_score = 100 * (1 - min(shoulder_tilt * 3, 1.0))
        hip_level_score = 100 * (1 - min(hip_tilt * 3, 1.0))
        
        # Weighted average
        final_score = (
            0.5 * alignment_score +
            0.3 * shoulder_level_score +
            0.2 * hip_level_score
        )
        
        return max(0, min(100, final_score))
    
    def analyze_frames(self, frames: List[np.ndarray]) -> float:
        """
        Analyze multiple frames and return average posture score.
        
        Args:
            frames: List of RGB frames
            
        Returns:
            Average posture score (0-100)
        """
        if not frames:
            return 0
        
        scores = []
        confidences = []
        
        for frame in frames:
            result = self.analyze_frame(frame)
            if result['detected'] and result['confidence'] > 0.5:
                scores.append(result['alignment_score'])
                confidences.append(result['confidence'])
        
        if not scores:
            # No valid detections
            return 50  # Neutral score
        
        # Weighted average by confidence
        weighted_score = np.average(scores, weights=confidences)
        
        return float(weighted_score)
    
    def __del__(self):
        """Clean up MediaPipe resources."""
        if hasattr(self, 'pose'):
            self.pose.close()


def analyze_posture(frames: List[np.ndarray]) -> float:
    """
    Convenience function to analyze posture from frames.
    
    Args:
        frames: List of RGB frames
        
    Returns:
        Posture score (0-100)
    """
    analyzer = PostureAnalyzer()
    score = analyzer.analyze_frames(frames)
    return score
