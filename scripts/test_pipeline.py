"""
Test Pipeline Script
====================
Quick smoke-test for the evaluate_interview() function.

Usage:
    python scripts/test_pipeline.py
    python scripts/test_pipeline.py path/to/your_video.mp4

Set OPENAI_API_KEY and GROQ_API_KEY in .env before running.
"""

import json
import sys
import os

# Allow running from project root
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ai_engine.pipeline import evaluate_interview


def main():
    # Accept an optional video path as CLI argument, else use the default
    video_path = sys.argv[1] if len(sys.argv) > 1 else "sample_video.mp4"

    print("=" * 60)
    print("  MentorAI — Interview Evaluation Pipeline Test")
    print("=" * 60)
    print(f"Video: {video_path}\n")

    if not os.path.exists(video_path):
        print(f"⚠  Video file not found: {video_path!r}")
        print("   Place a sample video at that path or pass one as an argument:")
        print("   python scripts/test_pipeline.py your_video.mp4")
        sys.exit(1)

    result = evaluate_interview(video_path)

    print("\n" + "=" * 60)
    print("  EVALUATION RESULT")
    print("=" * 60)
    print(json.dumps(result, indent=2, ensure_ascii=False))

    print("\n--- Summary ---")
    print(f"  Score    : {result['score']}/100")
    print(f"  Summary  : {result['summary']}")
    print(f"  Strengths: {result['strengths']}")
    print(f"  Weaknesses: {result['weaknesses']}")


if __name__ == "__main__":
    main()
