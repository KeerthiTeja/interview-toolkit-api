import random
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.db.models import Question, Session as InterviewSession, SessionQuestion


def create_session(db: Session, tag: str | None, difficulty: str | None, count: int):
    stmt = select(Question)

    if tag:
        stmt = stmt.where(Question.tag == tag)
    if difficulty:
        stmt = stmt.where(Question.difficulty == difficulty)

    questions = db.execute(stmt).scalars().all()

    if not questions:
        return None

    selected = random.sample(questions, k=min(count, len(questions)))

    session = InterviewSession()
    db.add(session)
    db.flush()  # important: ensures session.id exists

    for q in selected:
        db.add(SessionQuestion(session_id=session.id, question_id=q.id))

    db.commit()
    db.refresh(session)
    return session, selected
