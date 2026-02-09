# Mentor Scoring AI

A production-quality AI prototype for evaluating teacher/mentor performance from video.

## 🎯 Features

- **Posture Analysis**: Uses MediaPipe Pose to evaluate body posture and alignment
- **Voice Analysis**: Extracts pitch variance, energy, and speaking rate using Librosa
- **Content Evaluation**: Uses Ollama LLM (Mistral) for bilingual content quality assessment
- **Scalable Processing**: Handles both short (1-2 min) and long (30-60 min) videos
- **Real-time Feedback**: Progressive UI updates with non-blocking processing

## 🛠️ Tech Stack

- **Frontend**: Streamlit
- **Computer Vision**: MediaPipe (solutions.pose)
- **Speech-to-Text**: faster-whisper (base model, int8)
- **Audio Processing**: Librosa, ffmpeg
- **LLM**: Ollama (Mistral model)
- **Platform**: CPU-only, no GPU required

## 📋 Prerequisites

1. **Python 3.8+**
2. **ffmpeg** (for audio extraction)
   - Windows: Download from https://ffmpeg.org/download.html
   - Add to PATH
3. **Ollama** (for content evaluation)
   - Download from https://ollama.ai
   - Install and start: `ollama serve`
   - Pull Mistral model: `ollama pull mistral`

## 🚀 Installation

1. Clone or download this repository

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Verify Ollama is running:
```bash
ollama list
# Should show 'mistral' in the list
```

## ▶️ Usage

1. Start the Streamlit app:
```bash
streamlit run app.py
```

2. Open your browser (should open automatically at http://localhost:8501)

3. Upload an MP4 video file

4. Click "Analyze Video" and wait for results

## 📊 How It Works

### Processing Pipeline

1. **Video Preprocessing**
   - Extract audio (mono, 16kHz WAV)
   - Sample frames (1 frame every 5 seconds)

2. **Posture Analysis**
   - MediaPipe Pose detects body landmarks
   - Computes shoulder-hip alignment score

3. **Audio Analysis**
   - Extract pitch variance (expressiveness)
   - Measure RMS energy (volume)
   - Estimate speaking rate (pacing)

4. **Speech-to-Text**
   - Faster-whisper transcribes audio
   - Supports Hindi/Hinglish
   - Processes in 60-second chunks

5. **Content Evaluation**
   - Ollama LLM evaluates transcript
   - Scores: clarity, structure, technical accuracy, engagement
   - Bilingual prompt (Hindi + English)

6. **Final Scoring**
   - Weighted average:
     - Posture: 25%
     - Audio: 25%
     - Content: 30%
     - Engagement: 20%

## ⚙️ Configuration

Edit `config.py` to customize:
- Model parameters
- Chunk sizes
- Scoring weights
- Audio feature thresholds

## 🎬 Expected Performance

- **Short videos (1-2 min)**: First feedback in ~7-10 seconds
- **Long videos (30-60 min)**: 10-15 minutes total processing time
- **UI**: Never freezes, updates every 60 seconds

## 📁 Project Structure

```
mentorAI/
├── app.py                  # Streamlit entry point
├── config.py               # Configuration constants
├── pipeline.py             # Processing orchestrator
├── video_processor.py      # Audio extraction & frame sampling
├── posture_analyzer.py     # MediaPipe Pose analysis
├── audio_analyzer.py       # Librosa audio features
├── speech_to_text.py       # Faster-whisper transcription
├── content_evaluator.py    # Ollama LLM evaluation
├── scoring_engine.py       # Final score calculation
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## 🐛 Troubleshooting

### "Ollama is not running"
- Start Ollama: `ollama serve`
- Verify: `curl http://localhost:11434/api/tags`

### "Audio extraction failed"
- Ensure ffmpeg is installed and in PATH
- Test: `ffmpeg -version`

### "Model loading is slow"
- First run downloads faster-whisper model (~150MB)
- Subsequent runs use cached model

### "Out of memory"
- Reduce `AUDIO_CHUNK_DURATION` in config.py
- Reduce `MAX_FRAMES_PER_MINUTE` in config.py

## 📝 License

This is a prototype for educational/demonstration purposes.

## 🙏 Acknowledgments

- MediaPipe by Google
- Faster-Whisper by Guillaume Klein
- Ollama by Ollama Team
- Librosa by Brian McFee
