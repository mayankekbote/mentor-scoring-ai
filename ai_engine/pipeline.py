"""
AI Engine Pipeline
==================
Central entry point for the MentorAI backend evaluation service.

Public API
----------
    from ai_engine.pipeline import evaluate_interview

    result = evaluate_interview("path/to/interview.mp4")

Return Schema
-------------
{
    "score":           int,          # 0-100 overall score
    "strengths":       list[str],    # positive highlights
    "weaknesses":      list[str],    # areas for improvement
    "summary":         str,          # human-readable evaluation summary
    "transcript":      str,          # full audio transcript
    "audio_metrics":   dict,         # rms_energy, score
    "posture_metrics": dict          # frames_analyzed, detection_rate, score
}

Design Notes
------------
- No UI / streaming — synchronous blocking call, ideal for FastAPI endpoints.
- All heavy models are loaded lazily (first call only).
- Temporary audio files are cleaned up automatically in a finally block.
- Add `evaluate_interview` to a FastAPI route with zero code changes needed.

FastAPI integration example::

    from fastapi import FastAPI
    from ai_engine.pipeline import evaluate_interview

    app = FastAPI()

    @app.post("/evaluate")
    def evaluate(video_path: str):
        return evaluate_interview(video_path)
"""

from __future__ import annotations

import math
import os
import tempfile
from typing import Dict, List

import cv2
import ffmpeg
import librosa
import numpy as np
import soundfile as sf
from dotenv import load_dotenv

from ai_engine.evaluators.audio_analysis import analyze_audio
from ai_engine.evaluators.content_evaluation import (
    aggregate_chunk_evals,
    evaluate_content,
    generate_summary,
)
from ai_engine.evaluators.posture_analysis import analyze_posture
from ai_engine.models.whisper_client import WhisperClient

# ── Load environment variables from .env (no-op if already loaded) ─────────────
load_dotenv()

# ── Processing constants ────────────────────────────────────────────────────────
_AUDIO_SAMPLE_RATE = 16_000   # Hz — required by Whisper
_AUDIO_CHANNELS = 1            # Mono
_CHUNK_DURATION = 30           # seconds per transcript chunk
_FRAME_INTERVAL_SECS = 10      # sample one frame every N seconds
_MAX_FRAMES_PER_MIN = 6        # cap frames to avoid MediaPipe overload

# ── Scoring weights (must sum to 1.0) ──────────────────────────────────────────
_W_POSTURE = 0.25
_W_AUDIO = 0.25
_W_CONTENT = 0.30
_W_ENGAGEMENT = 0.20


# ═══════════════════════════════════════════════════════════════════════════════
# Public function
# ═══════════════════════════════════════════════════════════════════════════════

def evaluate_interview(video_path: str, on_progress: callable = None) -> Dict:
    """
    Run the full interview evaluation pipeline on a video file.
    
    Args:
        video_path: Absolute or relative path to the video file.
        on_progress: Optional callback function(progress_float, message_str)
    """
    def report(progress, message):
        if on_progress:
            on_progress(progress, message)
        print(f"[{progress*100:.0f}%] {message}")

    if not os.path.exists(video_path):
        raise FileNotFoundError(f"Video file not found: {video_path}")

    # Use a temporary directory that is always cleaned up
    with tempfile.TemporaryDirectory(prefix="mentorai_") as tmpdir:
        # ── Step 1: Extract audio ─────────────────────────────────────────────
        report(0.05, "Extracting audio from video...")
        audio_path = _extract_audio(video_path, tmpdir)

        # ── Step 2: Sample frames ─────────────────────────────────────────────
        report(0.15, "Sampling video frames for posture analysis...")
        frames, duration = _sample_frames(video_path)

        # ── Step 3: Audio analysis ────────────────────────────────────────────
        report(0.25, "Analysing audio quality...")
        audio_metrics = analyze_audio(audio_path)

        # ── Step 4: Posture analysis ──────────────────────────────────────────
        report(0.35, f"Analysing posture across {len(frames)} frames...")
        posture_metrics = analyze_posture(frames)

        # ── Step 5 & 6: Transcription + chunk evaluation ──────────────────────
        report(0.45, "Transcribing and evaluating content...")
        transcript, chunk_evals = _transcribe_and_evaluate(audio_path, duration, tmpdir, on_progress=on_progress)

        # ── Step 7: Aggregate content + generate summary ──────────────────────
        report(0.92, "Generating holistic summary...")
        aggregated = aggregate_chunk_evals(chunk_evals)
        summary_data = generate_summary(transcript)

        # ── Step 8: Final score ───────────────────────────────────────────────
        report(0.98, "Computing final score...")
        result = _build_result(
            audio_metrics=audio_metrics,
            posture_metrics=posture_metrics,
            aggregated_content=aggregated,
            summary_data=summary_data,
            transcript=transcript,
        )

    report(1.0, "Evaluation complete!")
    return result


# ═══════════════════════════════════════════════════════════════════════════════
# Private helpers
# ═══════════════════════════════════════════════════════════════════════════════

def _extract_audio(video_path: str, tmpdir: str) -> str:
    """Extract mono 16kHz WAV audio from *video_path* into *tmpdir*."""
    audio_path = os.path.join(tmpdir, "audio.wav")
    try:
        (
            ffmpeg
            .input(video_path)
            .output(
                audio_path,
                ac=_AUDIO_CHANNELS,
                ar=_AUDIO_SAMPLE_RATE,
                format="wav",
            )
            .overwrite_output()
            .run(quiet=True, capture_stdout=True, capture_stderr=True)
        )
    except ffmpeg.Error as exc:
        msg = exc.stderr.decode() if exc.stderr else str(exc)
        raise RuntimeError(f"Audio extraction failed: {msg}")
    return audio_path


def _sample_frames(video_path: str):
    """
    Sample RGB frames from *video_path* at regular intervals.

    Returns:
        (frames: list[np.ndarray], duration_secs: float)
    """
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise RuntimeError(f"Cannot open video: {video_path}")

    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = total_frames / fps

    interval = int(fps * _FRAME_INTERVAL_SECS)
    max_frames = max(1, int((duration / 60) * _MAX_FRAMES_PER_MIN))

    frames: List[np.ndarray] = []
    idx = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        if idx % interval == 0:
            frames.append(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            if len(frames) >= max_frames:
                break
        idx += 1

    cap.release()
    return frames, duration


def _transcribe_and_evaluate(audio_path: str, duration: float, tmpdir: str, on_progress: callable = None):
    """
    Transcribe audio in chunks and evaluate each chunk.

    Returns:
        (full_transcript: str, chunk_evals: list[dict])
    """
    whisper = WhisperClient()
    y, sr = librosa.load(audio_path, sr=_AUDIO_SAMPLE_RATE, mono=True)

    num_chunks = math.ceil(duration / _CHUNK_DURATION)
    chunk_transcripts: List[str] = []
    chunk_evals: List[Dict] = []

    for i in range(num_chunks):
        t_start = i * _CHUNK_DURATION
        t_end = min((i + 1) * _CHUNK_DURATION, duration)

        # Slice audio
        s_start = int(t_start * sr)
        s_end = int(t_end * sr)
        chunk_audio = y[s_start:s_end]

        chunk_wav = os.path.join(tmpdir, f"chunk_{i}.wav")
        sf.write(chunk_wav, chunk_audio, sr)

        # Progress: 45% to 90%
        progress = 0.45 + (i / num_chunks) * 0.45
        msg = f"Transcribing part {i+1} of {num_chunks}..."
        if on_progress:
            on_progress(progress, msg)
        print(f"    [{progress*100:.0f}%] {msg}")

        # Transcribe
        try:
            text = whisper.transcribe(chunk_wav)
        except Exception as exc:
            print(f"    ⚠ Transcription failed for chunk {i + 1}: {exc}")
            text = ""

        chunk_transcripts.append(text)

        # Evaluate content
        eval_result = evaluate_content(text)
        chunk_evals.append(eval_result)

        # Clean up chunk file
        try:
            os.remove(chunk_wav)
        except OSError:
            pass

    full_transcript = "\n\n".join(chunk_transcripts).strip()
    return full_transcript, chunk_evals


def _build_result(
    *,
    audio_metrics: Dict,
    posture_metrics: Dict,
    aggregated_content: Dict,
    summary_data: Dict,
    transcript: str,
) -> Dict:
    """Assemble the final structured result dictionary."""
    # Component scores
    audio_score = audio_metrics.get("score", 50.0)
    posture_score = posture_metrics.get("score", 50.0)
    clarity = aggregated_content.get("clarity", 50.0)
    structure = aggregated_content.get("structure", 50.0)
    technical = aggregated_content.get("technical", 50.0)
    engagement = aggregated_content.get("engagement", 50.0)

    content_score = (clarity + structure + technical) / 3.0

    # Weighted final score
    raw_score = (
        _W_POSTURE * posture_score
        + _W_AUDIO * audio_score
        + _W_CONTENT * content_score
        + _W_ENGAGEMENT * engagement
    )
    final_score = int(round(max(0.0, min(100.0, raw_score))))

    return {
        "score": final_score,
        "strengths": summary_data.get("strengths", []),
        "weaknesses": summary_data.get("weaknesses", []),
        "summary": summary_data.get("summary", ""),
        "transcript": transcript,
        "audio_metrics": {
            "rms_energy": audio_metrics.get("rms_energy"),
            "score": audio_score,
        },
        "posture_metrics": {
            "frames_analyzed": posture_metrics.get("frames_analyzed"),
            "frames_total": posture_metrics.get("frames_total"),
            "detection_rate": posture_metrics.get("detection_rate"),
            "score": posture_score,
        },
    }
