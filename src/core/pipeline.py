"""
Pipeline Module
Orchestrates chunked processing of video with progress tracking.
"""

import os
import numpy as np
from typing import Generator, Dict, List
import librosa
import soundfile as sf

from src import config
from src.core.video_processor import VideoProcessor
from src.analyzers.posture_analyzer import PostureAnalyzer
from src.analyzers.audio_analyzer import AudioAnalyzer
from src.models.speech_to_text import SpeechToText
from src.models.content_evaluator import ContentEvaluator
from src.core.scoring_engine import ScoringEngine


class ProcessingPipeline:
    """
    Orchestrates the complete video analysis pipeline.
    Processes video in chunks to ensure scalability and responsive UI.
    """
    
    def __init__(self, video_path: str):
        """
        Initialize processing pipeline.
        
        Args:
            video_path: Path to video file
        """
        self.video_path = video_path
        self.video_processor = VideoProcessor(video_path)
        
        # Initialize analyzers (models loaded lazily)
        self.posture_analyzer = PostureAnalyzer()
        self.stt = SpeechToText()
        self.content_evaluator = ContentEvaluator()
        self.scoring_engine = ScoringEngine()
        
        # Results storage
        self.audio_path = None
        self.frames = None
        self.duration = 0
        self.chunk_results = []
    
    def process(self) -> Generator[Dict, None, None]:
        """
        Process video in chunks with progress updates.
        
        Yields progress updates as dictionaries:
        - stage: Current processing stage
        - progress: Progress percentage (0-100)
        - message: Status message
        - chunk_result: Optional chunk result data
        - final_result: Optional final result (last yield)
        
        Design: This generator allows Streamlit to update UI incrementally
        without blocking.
        """
        try:
            # Stage 1: Video preprocessing
            yield {
                'stage': 'preprocessing',
                'progress': 0,
                'message': 'Extracting audio and sampling frames...'
            }
            
            self.audio_path = self.video_processor.extract_audio()
            self.frames, self.duration = self.video_processor.sample_frames()
            
            yield {
                'stage': 'preprocessing',
                'progress': 10,
                'message': f'Video preprocessed: {self.duration:.1f}s, {len(self.frames)} frames sampled'
            }
            
            # Stage 2: Posture analysis
            yield {
                'stage': 'posture',
                'progress': 15,
                'message': 'Analyzing posture...'
            }
            
            posture_score = self.posture_analyzer.analyze_frames(self.frames)
            
            yield {
                'stage': 'posture',
                'progress': 25,
                'message': f'Posture analysis complete: {posture_score:.1f}/100'
            }
            
            # Stage 3: Audio analysis
            yield {
                'stage': 'audio',
                'progress': 30,
                'message': 'Analyzing audio features...'
            }
            
            audio_analyzer = AudioAnalyzer(self.audio_path)
            audio_score = audio_analyzer.compute_score()
            
            yield {
                'stage': 'audio',
                'progress': 40,
                'message': f'Audio analysis complete: {audio_score:.1f}/100'
            }
            
            # Stage 4: Chunked transcription and content evaluation
            # This is the most time-consuming part
            num_chunks = int(np.ceil(self.duration / config.AUDIO_CHUNK_DURATION))
            
            chunk_transcripts = []
            chunk_evaluations = []
            
            for chunk_idx in range(num_chunks):
                start_time = chunk_idx * config.AUDIO_CHUNK_DURATION
                end_time = min((chunk_idx + 1) * config.AUDIO_CHUNK_DURATION, self.duration)
                
                # Progress calculation (40-90% for this stage)
                chunk_progress = 40 + int(50 * (chunk_idx / num_chunks))
                
                yield {
                    'stage': 'transcription',
                    'progress': chunk_progress,
                    'message': f'Processing segment {chunk_idx + 1}/{num_chunks} ({start_time:.0f}s - {end_time:.0f}s)...'
                }
                
                # Extract chunk audio
                chunk_audio_path = self._extract_audio_chunk(start_time, end_time, chunk_idx)
                
                # Transcribe chunk
                transcript = self.stt.get_full_transcript(chunk_audio_path)
                chunk_transcripts.append(transcript)
                
                # Evaluate content
                evaluation = self.content_evaluator.evaluate_content(transcript)
                chunk_evaluations.append(evaluation)
                
                # Clean up chunk file
                if os.path.exists(chunk_audio_path):
                    os.remove(chunk_audio_path)
                
                yield {
                    'stage': 'transcription',
                    'progress': chunk_progress + int(50 / num_chunks),
                    'message': f'Segment {chunk_idx + 1}/{num_chunks} complete',
                    'chunk_result': {
                        'chunk_idx': chunk_idx,
                        'transcript': transcript[:100] + '...' if len(transcript) > 100 else transcript,
                        'evaluation': evaluation
                    }
                }
            
            # Stage 5: Aggregate results
            yield {
                'stage': 'aggregation',
                'progress': 90,
                'message': 'Computing final scores...'
            }
            
            # Aggregate content evaluations
            aggregated_content = self._aggregate_evaluations(chunk_evaluations)
            
            # Compute final score
            final_result = self.scoring_engine.compute_final_score(
                posture_score,
                audio_score,
                aggregated_content
            )
            
            # Add interpretation and feedback
            final_result['interpretation'] = self.scoring_engine.get_score_interpretation(
                final_result['final_score']
            )
            final_result['feedback'] = self.scoring_engine.get_component_feedback(
                final_result['breakdown']
            )
            
            # Add full transcript
            final_result['full_transcript'] = '\n\n'.join(chunk_transcripts)
            final_result['content_summary'] = aggregated_content.get('summary', '')
            
            yield {
                'stage': 'complete',
                'progress': 100,
                'message': 'Analysis complete!',
                'final_result': final_result
            }
            
        except Exception as e:
            yield {
                'stage': 'error',
                'progress': 0,
                'message': f'Error: {str(e)}',
                'error': str(e)
            }
    
    def _extract_audio_chunk(self, start_time: float, end_time: float, chunk_idx: int) -> str:
        """
        Extract a time-based chunk from audio file.
        
        Args:
            start_time: Start time in seconds
            end_time: End time in seconds
            chunk_idx: Chunk index for filename
            
        Returns:
            Path to chunk audio file
        """
        # Load full audio
        y, sr = librosa.load(self.audio_path, sr=config.AUDIO_SAMPLE_RATE, mono=True)
        
        # Extract chunk samples
        start_sample = int(start_time * sr)
        end_sample = int(end_time * sr)
        chunk_audio = y[start_sample:end_sample]
        
        # Save chunk
        chunk_path = os.path.join(
            config.TEMP_DIR,
            f"chunk_{chunk_idx}.wav"
        )
        sf.write(chunk_path, chunk_audio, sr)
        
        return chunk_path
    
    def _aggregate_evaluations(self, evaluations: List[Dict]) -> Dict:
        """
        Aggregate multiple content evaluations.
        
        Args:
            evaluations: List of evaluation dicts
            
        Returns:
            Aggregated evaluation
        """
        # Filter successful evaluations
        valid_evals = [e for e in evaluations if e.get('success', False)]
        
        if not valid_evals:
            # Return neutral scores if all failed
            return {
                'clarity': 50,
                'structure': 50,
                'technical': 50,
                'engagement': 50,
                'summary': 'Content evaluation unavailable'
            }
        
        # Average scores
        aggregated = {
            'clarity': np.mean([e['clarity'] for e in valid_evals]),
            'structure': np.mean([e['structure'] for e in valid_evals]),
            'technical': np.mean([e['technical'] for e in valid_evals]),
            'engagement': np.mean([e['engagement'] for e in valid_evals]),
            'summary': ' | '.join([e['summary'] for e in valid_evals])
        }
        
        return aggregated
    
    def cleanup(self):
        """Clean up temporary files."""
        self.video_processor.cleanup()
        
        # Clean up any remaining chunk files
        for file in os.listdir(config.TEMP_DIR):
            if file.startswith('chunk_') and file.endswith('.wav'):
                try:
                    os.remove(os.path.join(config.TEMP_DIR, file))
                except Exception:
                    pass


def process_video_pipeline(video_path: str) -> Generator[Dict, None, None]:
    """
    Convenience function to process video through pipeline.
    
    Args:
        video_path: Path to video file
        
    Yields:
        Progress updates and final result
    """
    pipeline = ProcessingPipeline(video_path)
    
    try:
        for update in pipeline.process():
            yield update
    finally:
        pipeline.cleanup()
