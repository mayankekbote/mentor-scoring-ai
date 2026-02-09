"""
Scoring Engine Module
Aggregates all analysis scores into final mentor score.
"""

from typing import Dict
from src import config


class ScoringEngine:
    """
    Computes final mentor score from component scores.
    Uses weighted averaging based on configuration.
    """
    
    @staticmethod
    def compute_final_score(
        posture_score: float,
        audio_score: float,
        content_evaluation: Dict[str, float],
    ) -> Dict[str, any]:
        """
        Compute final mentor score with breakdown.
        
        Args:
            posture_score: Posture analysis score (0-100)
            audio_score: Audio quality score (0-100)
            content_evaluation: Dict with clarity, structure, technical, engagement scores
            
        Returns:
            Dictionary with:
            - final_score: Overall mentor score (0-100)
            - breakdown: Dict with component scores
            - weights: Dict with component weights
        """
        # Extract content scores
        clarity = content_evaluation.get('clarity', 50)
        structure = content_evaluation.get('structure', 50)
        technical = content_evaluation.get('technical', 50)
        engagement = content_evaluation.get('engagement', 50)
        
        # Average content scores
        content_score = (clarity + structure + technical) / 3
        
        # Calculate weighted final score
        final_score = (
            config.WEIGHT_POSTURE * posture_score +
            config.WEIGHT_AUDIO * audio_score +
            config.WEIGHT_CONTENT * content_score +
            config.WEIGHT_ENGAGEMENT * engagement
        )
        
        # Ensure bounds
        final_score = max(config.MIN_SCORE, min(config.MAX_SCORE, final_score))
        
        return {
            'final_score': round(final_score, 1),
            'breakdown': {
                'posture': round(posture_score, 1),
                'audio': round(audio_score, 1),
                'content': round(content_score, 1),
                'clarity': round(clarity, 1),
                'structure': round(structure, 1),
                'technical': round(technical, 1),
                'engagement': round(engagement, 1)
            },
            'weights': {
                'posture': config.WEIGHT_POSTURE,
                'audio': config.WEIGHT_AUDIO,
                'content': config.WEIGHT_CONTENT,
                'engagement': config.WEIGHT_ENGAGEMENT
            }
        }
    
    @staticmethod
    def get_score_interpretation(score: float) -> str:
        """
        Get human-readable interpretation of score.
        
        Args:
            score: Score (0-100)
            
        Returns:
            Interpretation string
        """
        if score >= 90:
            return "Excellent 🌟"
        elif score >= 80:
            return "Very Good 👍"
        elif score >= 70:
            return "Good ✓"
        elif score >= 60:
            return "Satisfactory 📊"
        elif score >= 50:
            return "Needs Improvement 📈"
        else:
            return "Requires Attention ⚠️"
    
    @staticmethod
    def get_component_feedback(breakdown: Dict[str, float]) -> Dict[str, str]:
        """
        Generate feedback for each component.
        
        Args:
            breakdown: Score breakdown dict
            
        Returns:
            Dict with feedback for each component
        """
        feedback = {}
        
        # Posture feedback
        posture = breakdown.get('posture', 0)
        if posture >= 80:
            feedback['posture'] = "Great posture! Maintains professional stance."
        elif posture >= 60:
            feedback['posture'] = "Good posture overall. Minor improvements possible."
        else:
            feedback['posture'] = "Consider improving posture alignment and stance."
        
        # Audio feedback
        audio = breakdown.get('audio', 0)
        if audio >= 80:
            feedback['audio'] = "Excellent voice quality and pacing."
        elif audio >= 60:
            feedback['audio'] = "Good audio quality. Voice is clear and well-paced."
        else:
            feedback['audio'] = "Consider improving voice modulation and speaking pace."
        
        # Content feedback
        clarity = breakdown.get('clarity', 0)
        structure = breakdown.get('structure', 0)
        technical = breakdown.get('technical', 0)
        
        if clarity >= 80:
            feedback['clarity'] = "Explanations are very clear and easy to understand."
        elif clarity >= 60:
            feedback['clarity'] = "Content is generally clear with room for improvement."
        else:
            feedback['clarity'] = "Focus on making explanations clearer and simpler."
        
        if structure >= 80:
            feedback['structure'] = "Well-structured content with logical flow."
        elif structure >= 60:
            feedback['structure'] = "Content has decent structure. Could be more organized."
        else:
            feedback['structure'] = "Improve content organization and logical flow."
        
        if technical >= 80:
            feedback['technical'] = "Strong technical accuracy and depth."
        elif technical >= 60:
            feedback['technical'] = "Technical content is adequate."
        else:
            feedback['technical'] = "Review technical accuracy and depth of explanations."
        
        # Engagement feedback
        engagement = breakdown.get('engagement', 0)
        if engagement >= 80:
            feedback['engagement'] = "Highly engaging teaching style!"
        elif engagement >= 60:
            feedback['engagement'] = "Reasonably engaging. Could use more interactive elements."
        else:
            feedback['engagement'] = "Work on making content more engaging with examples and questions."
        
        return feedback


def calculate_mentor_score(
    posture_score: float,
    audio_score: float,
    content_evaluation: Dict[str, float]
) -> Dict[str, any]:
    """
    Convenience function to calculate final mentor score.
    
    Args:
        posture_score: Posture score (0-100)
        audio_score: Audio score (0-100)
        content_evaluation: Content evaluation dict
        
    Returns:
        Complete scoring result with interpretation and feedback
    """
    engine = ScoringEngine()
    result = engine.compute_final_score(posture_score, audio_score, content_evaluation)
    
    # Add interpretation and feedback
    result['interpretation'] = engine.get_score_interpretation(result['final_score'])
    result['feedback'] = engine.get_component_feedback(result['breakdown'])
    
    return result
