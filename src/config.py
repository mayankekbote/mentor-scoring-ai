"""
Configuration module for Mentor Scoring AI.
Contains all constants and parameters used across the application.
"""

import os

# ============================================================================
# MODEL CONFIGURATIONS
# ============================================================================

# OpenAI Whisper API Configuration
# Set environment variable: OPENAI_API_KEY=your-key-here
# Cost: ~$0.006 per minute of audio
# Speed: 10x faster than CPU-based faster-whisper

# Groq API Configuration (for content evaluation)
# Set environment variable: GROQ_API_KEY=your-key-here
# Get free key at: https://console.groq.com/keys
# Speed: 10-20x faster than local Ollama
# Model: llama-3.1-8b-instant (very fast)

# MediaPipe Pose Configuration
MEDIAPIPE_STATIC_IMAGE_MODE = True
MEDIAPIPE_ENABLE_SEGMENTATION = False
MEDIAPIPE_SMOOTH_LANDMARKS = False
MEDIAPIPE_MIN_DETECTION_CONFIDENCE = 0.5
MEDIAPIPE_MIN_TRACKING_CONFIDENCE = 0.5

# ============================================================================
# PROCESSING PARAMETERS
# ============================================================================

# Audio Processing
AUDIO_SAMPLE_RATE = 16000  # Hz (required by faster-whisper)
AUDIO_CHANNELS = 1  # Mono
AUDIO_CHUNK_DURATION = 30  # seconds - reduced to 30s for faster UI updates

# Frame Sampling
FRAME_SAMPLE_INTERVAL = 10  # seconds - sample 1 frame every 10 seconds (reduced processing)
MAX_FRAMES_PER_MINUTE = 6  # Limit frames to prevent MediaPipe overload

# ============================================================================
# SCORING WEIGHTS
# ============================================================================

# Final score weighted calculation
WEIGHT_POSTURE = 0.25  # 25%
WEIGHT_AUDIO = 0.25    # 25%
WEIGHT_CONTENT = 0.30  # 30%
WEIGHT_ENGAGEMENT = 0.20  # 20%

# Score bounds
MIN_SCORE = 0
MAX_SCORE = 100

# ============================================================================
# FILE PATHS
# ============================================================================

# Temporary file storage
TEMP_DIR = "temp_processing"
UPLOAD_DIR = "uploads"

# Ensure directories exist
os.makedirs(TEMP_DIR, exist_ok=True)
os.makedirs(UPLOAD_DIR, exist_ok=True)

# ============================================================================
# UI CONFIGURATION
# ============================================================================

# Streamlit page config
PAGE_TITLE = "Mentor Scoring AI"
PAGE_ICON = "🎓"
LAYOUT = "wide"

# Progress update frequency
PROGRESS_UPDATE_INTERVAL = 1  # Update UI every chunk

# ============================================================================
# CONTENT EVALUATION PROMPT
# ============================================================================

# Bilingual prompt for Ollama (Hindi + English)
CONTENT_EVALUATION_PROMPT = """You are an expert educational content evaluator. Analyze the following transcript from a teaching session and provide scores.

The transcript may contain Hindi, English, or Hinglish (mixed). Evaluate based on:

1. **Clarity** (0-100): How clear and understandable is the explanation?
2. **Structure** (0-100): Is the content well-organized with logical flow?
3. **Technical Accuracy** (0-100): Are concepts explained correctly?
4. **Engagement** (0-100): Does the teacher use engaging language, examples, or questions?

Transcript:
{transcript}

Respond ONLY with valid JSON in this exact format:
{{
  "clarity": <number 0-100>,
  "structure": <number 0-100>,
  "technical": <number 0-100>,
  "engagement": <number 0-100>,
  "summary": "<brief 1-2 sentence summary in English>"
}}
"""

# ============================================================================
# AUDIO FEATURE THRESHOLDS
# ============================================================================

# These thresholds are used to normalize audio features to 0-100 scores
# Tuned for typical teaching scenarios

PITCH_VARIANCE_MIN = 10  # Hz - monotone
PITCH_VARIANCE_MAX = 150  # Hz - very expressive
PITCH_VARIANCE_OPTIMAL = 80  # Hz - good variation

RMS_ENERGY_MIN = 0.01  # Very quiet
RMS_ENERGY_MAX = 0.3   # Very loud
RMS_ENERGY_OPTIMAL = 0.1  # Good volume

SPEAKING_RATE_MIN = 1.0  # syllables per second - very slow
SPEAKING_RATE_MAX = 5.0  # syllables per second - very fast
SPEAKING_RATE_OPTIMAL = 3.0  # syllables per second - good pace
