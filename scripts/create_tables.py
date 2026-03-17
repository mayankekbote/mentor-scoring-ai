from backend.database import engine, Base
# Import models to ensure they are registered with Base.metadata
from backend.models.user import User
from backend.models.admin import Admin
from backend.models.interview_code import InterviewCode
from backend.models.submission import Submission
from backend.models.evaluation_result import AIResult
from backend.models.password_reset import PasswordReset

def init_db():
    print("Initializing database...")
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully.")

if __name__ == "__main__":
    init_db()
