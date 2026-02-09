# Mentor Scoring AI

Production-quality AI prototype for evaluating teacher/mentor performance from video.

## 🚀 Quick Start

**📖 Complete setup instructions**: See **[docs/SETUP_GUIDE.md](docs/SETUP_GUIDE.md)**

### TL;DR

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Create `.env` file** (copy from `.env.example`):
   ```
   OPENAI_API_KEY=your-key-here
   GROQ_API_KEY=your-key-here
   ```

3. **Run:**
   ```bash
   streamlit run app.py
   ```

## 📖 Documentation

- **[SETUP_GUIDE.md](docs/SETUP_GUIDE.md)** - Complete installation and usage guide ⭐
- **[RESTRUCTURING.md](docs/RESTRUCTURING.md)** - Project structure explanation

## 🎯 Features

- **Posture Analysis**: MediaPipe Pose for body alignment scoring
- **Voice Analysis**: RMS energy extraction for volume quality
- **Speech-to-Text**: OpenAI Whisper API (10x faster than CPU)
- **Content Evaluation**: Groq API for teaching quality assessment (20x faster than local LLM)
- **Progressive UI**: Real-time updates during processing
- **Scalable**: Handles 1-60 minute videos efficiently

## 📁 Project Structure

```
mentorAI/
├── app.py                    # Streamlit web application (entry point)
├── requirements.txt          # Python dependencies
├── .env.example             # API keys template
├── .env                     # Your API keys (create this)
│
├── src/                     # Source code
│   ├── config.py           # Configuration
│   ├── core/               # Core logic (pipeline, video, scoring)
│   ├── analyzers/          # Posture & audio analysis
│   └── models/             # AI model wrappers (OpenAI, Groq)
│
├── docs/                    # Documentation
│   ├── SETUP_GUIDE.md      # Complete setup guide
│   └── RESTRUCTURING.md    # Project structure
│
└── scripts/                 # Helper scripts
    └── run_app.ps1         # Windows launcher
```

## 📊 Performance

**Processing time for 6-minute video:**
- Transcription: ~24 seconds (OpenAI Whisper)
- Content evaluation: ~36 seconds (Groq)
- Audio + Posture: ~5 seconds
- **Total: ~65 seconds**

## 🛠️ Tech Stack

- **Frontend**: Streamlit
- **Speech-to-Text**: OpenAI Whisper API
- **Content Evaluation**: Groq API (llama-3.1-8b-instant)
- **Posture Analysis**: MediaPipe Pose
- **Audio Processing**: librosa
- **Video Processing**: ffmpeg, opencv

## 📝 License

Educational prototype - built for demonstration purposes.
