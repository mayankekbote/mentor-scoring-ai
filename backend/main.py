from dotenv import load_dotenv
load_dotenv()
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.routes import auth, interview, upload, admin

app = FastAPI(
    title="AI Interview Submission Platform",
    description="API for managing interview submissions and AI evaluations.",
    version="0.1.0",
)

# ---------------------------------------------------------------------------
# CORS — allow React dev server during development
# ---------------------------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# Routers
# ---------------------------------------------------------------------------
app.include_router(auth.router, prefix="/api/auth", tags=["Auth"])
app.include_router(interview.router, prefix="/api/interview", tags=["Interview"])
app.include_router(upload.router, prefix="/api/upload", tags=["Upload"])
app.include_router(admin.router, prefix="/api/admin", tags=["Admin"])


@app.get("/", tags=["Health"])
async def health_check():
    return {"status": "ok", "message": "AI Interview Submission Platform is running."}
