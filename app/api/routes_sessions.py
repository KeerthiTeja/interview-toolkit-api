from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.schemas.sessions import SessionCreate, SessionOut
from app.db.deps import get_db
from app.services.session_generator import create_session
from app.db.models import Session as InterviewSession, SessionQuestion

router = APIRouter(prefix="/sessions", tags=["sessions"])

@router.post("", response_model=SessionOut, status_code=201)
def create_interview_session(payload: SessionCreate, db: Session = Depends(get_db)):
    result = create_session(db, payload.tag, payload.difficulty, payload.count)

    if not result:
        raise HTTPException(status_code=404, detail="No questions found for given filters")

    session, questions = result

    return {
        "id": session.id,
        "created_at": session.created_at,
        "question_ids": [q.id for q in questions],
    }

@router.get("/{session_id}", response_model=SessionOut)
def get_session(session_id: int, db: Session = Depends(get_db)):
    session = db.get(InterviewSession, session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    stmt = select(SessionQuestion).where(SessionQuestion.session_id == session_id)
    links = db.execute(stmt).scalars().all()

    question_ids = [link.question_id for link in links]

    return {
        "id": session.id,
        "created_at": session.created_at,
        "question_ids": question_ids,
    }