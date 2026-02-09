"""
Mentor Scoring AI - Streamlit Application
Main entry point for the web interface.
"""

import streamlit as st
import os
import time
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from src import config
from src.core.pipeline import process_video_pipeline
from src.models.content_evaluator import ContentEvaluator


# Page configuration
st.set_page_config(
    page_title=config.PAGE_TITLE,
    page_icon=config.PAGE_ICON,
    layout=config.LAYOUT
)


def check_dependencies():
    """
    Check if all required dependencies are available.
    
    Returns:
        Tuple of (success: bool, message: str)
    """
    # Check Groq API key
    import os
    if not os.getenv("GROQ_API_KEY"):
        return False, """
        ⚠️ **Groq API key is not set.**
        
        Please set your Groq API key:
        1. Get free key: https://console.groq.com/keys
        2. Set environment variable:
           ```
           $env:GROQ_API_KEY="your-key-here"
           ```
        3. Restart the app
        
        Groq is 10-20x faster than local Ollama!
        """
    
    return True, "All dependencies available ✓"


def save_uploaded_file(uploaded_file) -> str:
    """
    Save uploaded file to disk.
    
    Args:
        uploaded_file: Streamlit UploadedFile object
        
    Returns:
        Path to saved file
    """
    # Create unique filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{timestamp}_{uploaded_file.name}"
    filepath = os.path.join(config.UPLOAD_DIR, filename)
    
    # Save file
    with open(filepath, 'wb') as f:
        f.write(uploaded_file.getbuffer())
    
    return filepath


def display_results(result: dict):
    """
    Display final analysis results.
    
    Args:
        result: Final result dictionary from pipeline
    """
    # Main score display
    st.markdown("---")
    st.markdown("## 🎯 Final Mentor Score")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        # Large score display
        score = result['final_score']
        st.markdown(f"""
        <div style='text-align: center; padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 10px;'>
            <h1 style='color: white; font-size: 72px; margin: 0;'>{score}</h1>
            <p style='color: white; font-size: 24px; margin: 0;'>/100</p>
            <p style='color: white; font-size: 18px; margin-top: 10px;'>{result['interpretation']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # Score breakdown
        st.markdown("### 📊 Score Breakdown")
        breakdown = result['breakdown']
        
        # Component scores with progress bars
        st.markdown(f"**Posture:** {breakdown['posture']}/100")
        st.progress(breakdown['posture'] / 100)
        
        st.markdown(f"**Audio Quality:** {breakdown['audio']}/100")
        st.progress(breakdown['audio'] / 100)
        
        st.markdown(f"**Content Quality:** {breakdown['content']}/100")
        st.progress(breakdown['content'] / 100)
        
        st.markdown(f"**Engagement:** {breakdown['engagement']}/100")
        st.progress(breakdown['engagement'] / 100)
    
    # Detailed feedback
    st.markdown("---")
    st.markdown("## 💡 Detailed Feedback")
    
    feedback = result['feedback']
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🧍 Posture")
        st.info(feedback['posture'])
        
        st.markdown("### 🎤 Audio Quality")
        st.info(feedback['audio'])
    
    with col2:
        st.markdown("### 📚 Content Quality")
        st.info(feedback['clarity'])
        st.info(feedback['structure'])
        st.info(feedback['technical'])
        
        st.markdown("### 🎯 Engagement")
        st.info(feedback['engagement'])
    
    # Content summary
    if result.get('content_summary'):
        st.markdown("---")
        st.markdown("## 📝 Content Summary")
        st.write(result['content_summary'])
    
    # Full transcript (expandable)
    if result.get('full_transcript'):
        st.markdown("---")
        with st.expander("📄 View Full Transcript"):
            st.text_area(
                "Transcript",
                result['full_transcript'],
                height=300,
                label_visibility="collapsed"
            )


def main():
    """Main application logic."""
    
    # Header
    st.title("🎓 Mentor Scoring AI")
    st.markdown("""
    Evaluate teaching performance from video using AI-powered analysis of:
    - **Body posture** (MediaPipe)
    - **Voice quality** (Librosa)
    - **Content quality** (Ollama LLM)
    """)
    
    # Check dependencies
    deps_ok, deps_msg = check_dependencies()
    if not deps_ok:
        st.error(deps_msg)
        st.stop()
    else:
        st.success(deps_msg)
    
    st.markdown("---")
    
    # File upload
    st.markdown("### 📹 Upload Video")
    uploaded_file = st.file_uploader(
        "Choose a video file (MP4)",
        type=['mp4'],
        help="Upload a teaching/mentoring video (1-60 minutes)"
    )
    
    if uploaded_file is not None:
        # Display video info
        file_size_mb = uploaded_file.size / (1024 * 1024)
        st.info(f"**File:** {uploaded_file.name} ({file_size_mb:.1f} MB)")
        
        # Process button
        if st.button("🚀 Analyze Video", type="primary"):
            # Save uploaded file
            with st.spinner("Saving video..."):
                video_path = save_uploaded_file(uploaded_file)
            
            st.success(f"Video saved: {video_path}")
            
            # Processing section
            st.markdown("---")
            st.markdown("### ⚙️ Processing")
            
            # Create placeholders for dynamic updates
            progress_bar = st.progress(0)
            status_text = st.empty()
            chunk_info = st.empty()
            
            # Process video through pipeline
            try:
                final_result = None
                
                for update in process_video_pipeline(video_path):
                    # Update progress bar
                    progress_bar.progress(update['progress'] / 100)
                    
                    # Update status text
                    status_text.markdown(f"**Status:** {update['message']}")
                    
                    # Display chunk results if available
                    if 'chunk_result' in update:
                        chunk = update['chunk_result']
                        chunk_info.info(
                            f"Segment {chunk['chunk_idx'] + 1}: {chunk['transcript']}"
                        )
                    
                    # Store final result
                    if 'final_result' in update:
                        final_result = update['final_result']
                    
                    # Check for errors
                    if update['stage'] == 'error':
                        st.error(f"Processing failed: {update['message']}")
                        break
                    
                    # Small delay to make updates visible
                    time.sleep(0.1)
                
                # Display results
                if final_result:
                    status_text.markdown("**Status:** ✅ Analysis complete!")
                    display_results(final_result)
                    
                    # Clean up uploaded file
                    try:
                        os.remove(video_path)
                    except Exception:
                        pass
                
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
                import traceback
                with st.expander("Error Details"):
                    st.code(traceback.format_exc())
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: gray; font-size: 12px;'>
        <p>Mentor Scoring AI v1.0 | Built with Streamlit, MediaPipe, Faster-Whisper, and Ollama</p>
        <p>CPU-optimized for production use | No GPU required</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
