# AI Interview Submission Platform — Project Walkthrough

## Phase 1: Architecture & Scaffolding (Completed)
The project structure has been established with a clear separation between the frontend (React), backend (FastAPI), and the existing AI engine.

## Phase 2: Database Schema & Models (Completed)
The database schema has been implemented using SQLAlchemy ORM and Pydantic schemas.

### Database Architecture
- **Users Table**: Stores core account details. All registered users are candidates by default.
- **Admins Table**: Extends the `Users` table. Users in this table have admin/HR privileges.
- **Interview Codes**: Managed by admins; used by candidates to gain submission access.
- **Submissions**: Links candidates to interview codes. Enforces a **one submission per code** constraint.
- **AI Results**: Stores detailed evaluation metrics. Designed for admin-only access.
- **Password Resets**: Handles secure password recovery tokens.

### Implementation Details
- **SQLAlchemy Models**: Located in `backend/models/`. Includes relationship mapping and unique constraints.
- **Pydantic Schemas**: Located in `backend/schemas/`. Provides validation for requests and responses.
- **Database Initialization**: A script `scripts/create_tables.py` is provided to initialize the schema.

### Verification Results
- Successfully installed dependencies and ran the initialization script.
- Confirmed that all tables were created in the PostgreSQL database (`mentora`).

## Next Steps
- **User Authentication**: Implement registration and login flows with JWT.
- **Interview Workflow**: Implement the logic for validating interview codes and handling video uploads.
- **AI Integration**: Connect the backend to the `ai_engine` to trigger evaluations on submission.
