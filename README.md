# MentorAI — Intelligent Interview Evaluation Platform

MentorAI is a full-stack platform designed to automate the evaluation of teaching and speaking demonstrations using AI. It analyzes video submissions for content accuracy, vocal clarity, and body language, providing structured feedback and scores for candidates.

## 🚀 Presentation Features
- **AI Video Pipeline**: Automated processing using OpenAI Whisper (Transcription) and Groq (LLM Analysis).
- **Physical Analysis**: MediaPipe for posture and confidence scoring.
- **Vocal Metrics**: Volume and energy analysis via Librosa.
- **Admin Dashboard**: Comprehensive management of candidates, interview codes, and organization-scoped data.
- **Interview Invitations**: One-click automated scheduling with professional HTML email invitations.

---

## 🛠️ Tech Stack
- **Frontend**: React.js, Vite, TailwindCSS, Lucide Icons.
- **Backend**: FastAPI (Python), SQLAlchemy, PostgreSQL/SQLite.
- **AI Layer**: OpenAI Whisper, Groq (Llama-3), MediaPipe, CV2.

---

## 📋 Prerequisites
Before you begin, ensure you have the following installed on your machine:
- **Python 3.10+**
- **Node.js (v18+)** & **npm**
- **PostgreSQL** (Optional — SQLite is default for dev)
- **FFmpeg**: **Required** for video processing.
  - *Windows*: `choco install ffmpeg` or download from [ffmpeg.org](https://ffmpeg.org/download.html).
  - *macOS*: `brew install ffmpeg`
  - *Linux*: `sudo apt install ffmpeg`

---

## ⚙️ Installation & Setup

### 1. Clone the Repository
```bash
git clone <repository-url>
cd mentorAI
```

### 2. Backend Setup
1. **Create a Virtual Environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
2. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Environment Configuration:**
   - Copy `.env.example` to `.env`:
     ```bash
     cp .env.example .env
     ```
   - Open `.env` and fill in your API keys:
     - `OPENAI_API_KEY`: For Whisper transcription.
     - `GROQ_API_KEY`: For high-speed LLM evaluation.
     - `DATABASE_URL`: Your Postgres or SQLite connection string.
     - `SMTP` settings: Required for invitation emails.

### 3. Frontend Setup
1. **Navigate to the frontend directory:**
   ```bash
   cd frontend
   ```
2. **Install npm packages:**
   ```bash
   npm install
   ```

---

## 🏃 Running the Project

### 1. Start the Backend
From the root directory (`mentorAI`):
```bash
uvicorn backend.main:app --reload
```
- API will be available at `http://localhost:8000`
- Interactive API Docs: `http://localhost:8000/docs`

### 2. Start the Frontend
From the `frontend` directory:
```bash
npm run dev
```
- Application will start at `http://localhost:5173`

---

## 📁 Project Structure
- `/backend`: FastAPI server, SQLAlchemy models, and API routes.
- `/frontend`: React application with Vite and Tailwind.
- `/ai_engine`: Core AI logic for video, audio, and content analysis.
- `/storage`: Local directory for uploaded videos and temporary processing files.

---

## 📝 Credentials
- **Admin Registration**: You can create the first admin using the signup page.
- **Organizations**: All data is isolated by `organization_name` provided during registration.

## ⚠️ Important Note
Ensure **FFmpeg** is in your system's PATH. Without it, the AI engine will fail to extract audio and frames from the uploaded videos.
