"""
upload.py — Video upload routes
Handles: receiving video file, storing to disk, triggering AI evaluation
"""
from fastapi import APIRouter

router = APIRouter()


@router.get("/ping")
async def ping():
    # TODO: implement video upload endpoint
    return {"route": "upload", "status": "placeholder"}
