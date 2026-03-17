import os
import logging
from sqlalchemy.orm import Session
from backend.database import SessionLocal
from backend.models.submission import Submission
from backend.models.evaluation_result import AIResult
from ai_engine.pipeline import evaluate_interview

# Configure logging to see AI progress in console
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def process_submission_evaluation(submission_id: int):
    """
    Background task to run AI evaluation and store results.
    """
    db = SessionLocal()
    submission = None
    try:
        submission = db.query(Submission).filter(Submission.id == submission_id).first()
        if not submission:
            logger.error(f"Submission {submission_id} not found for AI processing")
            return

        def update_progress(progress, message):
            # We use a fresh session or the existing one to update progress
            # To avoid threading issues with the main evaluation, we can use a new session
            # but since this is already in a background task thread, we can just use the current one
            try:
                # Re-fetch to ensure we have the latest state and aren't detached
                sub = db.query(Submission).filter(Submission.id == submission_id).first()
                if sub:
                    sub.processing_progress = progress
                    sub.processing_message = message
                    db.commit()
            except Exception as e:
                logger.error(f"Failed to update progress for {submission_id}: {e}")

        # Update status to processing
        submission.status = "processing"
        submission.processing_progress = 0.01
        submission.processing_message = "Initializing engine..."
        db.commit()
        
        logger.info(f"Starting AI evaluation for submission {submission_id}")
        
        # Get absolute path for processing
        video_abs_path = os.path.abspath(submission.video_url)
        
        # Call the existing AI engine pipeline with callback
        results = evaluate_interview(video_abs_path, on_progress=update_progress)
        
        # Store results in the database
        ai_result = AIResult(
            submission_id=submission.id,
            score=results.get("score"),
            strengths=results.get("strengths"),
            weaknesses=results.get("weaknesses"),
            summary=results.get("summary"),
            transcript=results.get("transcript"),
            audio_metrics=results.get("audio_metrics"),
            posture_metrics=results.get("posture_metrics")
        )
        
        db.add(ai_result)
        
        # Update submission status
        submission.status = "completed"
        submission.processing_progress = 1.0
        submission.processing_message = "Completed"
        db.commit()
        
        logger.info(f"AI evaluation for submission {submission_id} completed.")
        
    except Exception as e:
        logger.error(f"Critical error during AI processing for submission {submission_id}: {str(e)}")
        if submission:
            submission.status = "failed"
            db.commit()
    finally:
        db.close()
