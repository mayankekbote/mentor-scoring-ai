"""Test MediaPipe import"""
try:
    print("Testing MediaPipe import...")
    import mediapipe as mp
    print("✓ MediaPipe imported successfully!")
    print(f"MediaPipe version: {mp.__version__}")
    
    print("\nTesting Pose...")
    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose(static_image_mode=True)
    print("✓ Pose initialized successfully!")
    pose.close()
    
except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()
