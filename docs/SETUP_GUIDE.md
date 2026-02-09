# Mentor Scoring AI - Complete Setup Guide

A production-quality AI system for evaluating teacher/mentor performance from video using posture analysis, voice analysis, and content evaluation.

---

## 📋 Table of Contents

1. [Prerequisites](#prerequisites)
2. [Installation](#installation)
3. [API Keys Setup](#api-keys-setup)
4. [Running the Application](#running-the-application)
5. [Using the Application](#using-the-application)
6. [Troubleshooting](#troubleshooting)
7. [Project Structure](#project-structure)

---

## 🔧 Prerequisites

Before you begin, ensure you have:

- **Python 3.10 or higher** installed
  - Check: `python --version`
  - Download from: https://www.python.org/downloads/

- **ffmpeg** installed (for video processing)
  - **Windows**: Download from https://ffmpeg.org/download.html
  - **Mac**: `brew install ffmpeg`
  - **Linux**: `sudo apt install ffmpeg`
  - Check: `ffmpeg -version`

---

## 📦 Installation

### Step 1: Clone or Download the Project

```bash
cd path/to/mentorAI
```

### Step 2: Create a Virtual Environment (Recommended)

**Windows:**
```powershell
python -m venv venv
.\\venv\\Scripts\\Activate.ps1
```

**Mac/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- `streamlit` - Web interface
- `python-dotenv` - Environment variable management
- `openai` - OpenAI Whisper API (speech-to-text)
- `groq` - Groq API (fast LLM for content evaluation)
- `mediapipe` - Posture analysis
- `opencv-python` - Video processing
- `librosa` - Audio analysis
- `soundfile` - Audio I/O
- `ffmpeg-python` - Video/audio extraction
- `numpy` - Numerical operations
- `tensorflow` - MediaPipe dependency
- `protobuf` - Protocol buffers

**Installation time**: ~2-5 minutes depending on your internet speed.

---

## 🔑 API Keys Setup

You need two free API keys:

### 1. OpenAI API Key (for Speech-to-Text)

1. Go to: https://platform.openai.com/api-keys
2. Sign in or create an account
3. Click **"Create new secret key"**
4. Copy the key (starts with `sk-...`)
5. **Cost**: ~$0.006 per minute of audio

### 2. Groq API Key (for Content Evaluation)

1. Go to: https://console.groq.com/keys
2. Sign up (completely free!)
3. Click **"Create API Key"**
4. Copy the key (starts with `gsk_...`)
5. **Cost**: FREE (generous free tier)

### 3. API Keys are Already Configured!

The `.env` file is **already included** in this repository with working API keys for your team.

**You don't need to do anything!** The keys are:
- ✅ OpenAI API Key (for speech-to-text)
- ✅ Groq API Key (for content evaluation)

**Note**: If you want to use your own keys later, simply edit the `.env` file.

---

## 🚀 Running the Application

### Method 1: Direct Command

```bash
streamlit run app.py
```

### Method 2: Using Helper Script (Windows)

```powershell
.\\scripts\\run_app.ps1
```

### What to Expect

The terminal will show:
```
You can now view your Streamlit app in your browser.

Local URL: http://localhost:8501
Network URL: http://192.168.x.x:8501
```

The app will automatically open in your default browser.

---

## 🎯 Using the Application

### Step 1: Upload Video

1. Click **"Browse files"** or drag-and-drop
2. Supported formats: MP4, AVI, MOV
3. Recommended: 1-10 minute videos for best results

### Step 2: Start Analysis

1. Click **"Analyze Video"** button
2. Watch real-time progress updates

### Step 3: View Results

The system analyzes:

1. **Posture** (25% weight)
   - Body alignment using MediaPipe Pose
   - Shoulder-hip vertical alignment

2. **Voice Quality** (25% weight)
   - Volume/energy levels
   - Audio clarity

3. **Content Quality** (30% weight)
   - Clarity of explanation
   - Logical structure
   - Technical accuracy
   - Student engagement

4. **Engagement Trend** (20% weight)
   - Consistency across video segments

### Results Display

- **Overall Score**: 0-100 rating
- **Component Breakdown**: Individual scores
- **Transcript**: Full speech-to-text output
- **Summary**: AI-generated feedback

---

## ⚡ Performance

**Processing Time Examples:**

| Video Length | Processing Time |
|--------------|-----------------|
| 1 minute | ~10-15 seconds |
| 5 minutes | ~45-60 seconds |
| 10 minutes | ~1.5-2 minutes |
| 30 minutes | ~4-6 minutes |

**What happens during processing:**

1. **Preprocessing** (~5 seconds)
   - Extract audio from video
   - Sample frames every 10 seconds

2. **Posture Analysis** (~2-5 seconds)
   - Analyze sampled frames with MediaPipe

3. **Audio Analysis** (~1-2 seconds)
   - Extract volume/energy features

4. **Per-Segment Processing** (30-second chunks)
   - Transcribe audio (OpenAI Whisper): ~2-3 seconds
   - Evaluate content (Groq LLM): ~2-3 seconds

5. **Final Scoring** (~1 second)
   - Aggregate all scores

---

## 🐛 Troubleshooting

### Issue: "OPENAI_API_KEY environment variable not set"

**Solution:**
1. Check `.env` file exists in project root
2. Verify key is correct (starts with `sk-`)
3. Restart the application

### Issue: "GROQ_API_KEY environment variable not set"

**Solution:**
1. Check `.env` file has Groq key
2. Verify key is correct (starts with `gsk_`)
3. Get free key from: https://console.groq.com/keys

### Issue: "ffmpeg not found"

**Solution:**
1. Install ffmpeg (see Prerequisites)
2. Add ffmpeg to system PATH
3. Restart terminal/PowerShell

### Issue: "ModuleNotFoundError"

**Solution:**
```bash
pip install -r requirements.txt
```

### Issue: "Protobuf compatibility error"

**Solution:**
```bash
pip install --force-reinstall tensorflow==2.15.0 protobuf==4.23.4 mediapipe==0.10.9
```

### Issue: Processing is slow

**Causes:**
- Large video file (>100MB)
- Long video (>30 minutes)
- Slow internet (API calls)

**Solutions:**
- Use shorter clips for testing
- Check internet connection
- Ensure no other heavy processes running

---

## 📁 Project Structure

```
mentorAI/
├── app.py                    # Main Streamlit application
├── requirements.txt          # Python dependencies
├── .env.example             # API keys template
├── .env                     # Your API keys (create this)
├── .gitignore               # Git ignore rules
│
├── src/                     # Source code
│   ├── config.py           # Configuration
│   ├── core/               # Core logic
│   │   ├── pipeline.py     # Processing orchestration
│   │   ├── video_processor.py  # Video/audio extraction
│   │   └── scoring_engine.py   # Score calculation
│   ├── analyzers/          # Analysis modules
│   │   ├── posture_analyzer.py # MediaPipe Pose
│   │   └── audio_analyzer.py   # Audio features
│   └── models/             # AI model wrappers
│       ├── speech_to_text.py   # OpenAI Whisper
│       └── content_evaluator.py # Groq LLM
│
├── docs/                    # Documentation
└── scripts/                 # Helper scripts
    └── run_app.ps1         # Windows launcher
```

---

## 🎓 How It Works

### Architecture Overview

```
Video Upload
    ↓
Preprocessing (extract audio + sample frames)
    ↓
┌─────────────────┬──────────────────┬─────────────────┐
│  Posture        │  Audio           │  Content        │
│  Analysis       │  Analysis        │  Evaluation     │
│  (MediaPipe)    │  (librosa)       │  (per segment)  │
│                 │                  │                 │
│  • Sample       │  • Extract       │  • Transcribe   │
│    frames       │    RMS energy    │    (OpenAI)     │
│  • Detect       │  • Compute       │  • Evaluate     │
│    landmarks    │    score         │    (Groq)       │
│  • Score        │                  │                 │
│    alignment    │                  │                 │
└─────────────────┴──────────────────┴─────────────────┘
                    ↓
            Scoring Engine
         (weighted aggregation)
                    ↓
            Final Results
```

### Technology Stack

- **Frontend**: Streamlit (Python web framework)
- **Speech-to-Text**: OpenAI Whisper API
- **Content Evaluation**: Groq API (llama-3.1-8b-instant)
- **Posture Analysis**: MediaPipe Pose
- **Audio Processing**: librosa
- **Video Processing**: ffmpeg, opencv

---

## 💡 Tips for Best Results

1. **Video Quality**
   - Good lighting
   - Clear audio
   - Stable camera position
   - Speaker visible in frame

2. **Video Length**
   - 2-10 minutes ideal for testing
   - Longer videos work but take more time

3. **Content**
   - Teaching/mentoring sessions work best
   - Clear speech (Hindi/English supported)
   - Structured presentation

---

## 📞 Support

For issues or questions:
1. Check the Troubleshooting section above
2. Verify all prerequisites are installed
3. Ensure API keys are correctly set in `.env`

---

## 📝 Notes

- **Privacy**: Videos are processed locally, only audio is sent to APIs
- **Cost**: ~$0.01-0.05 per 10-minute video (OpenAI charges only)
- **Languages**: Auto-detects Hindi and English
- **Offline**: Requires internet for OpenAI and Groq APIs

---

**Ready to start!** Follow the installation steps above and you'll be analyzing videos in minutes.
