"""
Quick Test Script
Tests individual components to identify bottlenecks.
"""

import time

print("Testing component load times...\n")

# Test 1: Faster-whisper model loading
print("1. Testing faster-whisper model loading...")
start = time.time()
from faster_whisper import WhisperModel
model = WhisperModel("base", device="cpu", compute_type="int8")
print(f"   ✓ Loaded in {time.time() - start:.2f}s")

# Test 2: MediaPipe
print("\n2. Testing MediaPipe...")
start = time.time()
import mediapipe as mp
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(static_image_mode=True)
pose.close()
print(f"   ✓ Loaded in {time.time() - start:.2f}s")

# Test 3: Librosa
print("\n3. Testing Librosa...")
start = time.time()
import librosa
print(f"   ✓ Loaded in {time.time() - start:.2f}s")

print("\n✓ All components loaded successfully!")
print("\nNote: First-time faster-whisper run downloads ~150MB model.")
print("Subsequent runs will be much faster (model is cached).")
