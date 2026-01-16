from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.schemas.questions import QuestionCreate, QuestionOut
from app.db.models import Question
from app.db.deps import get_db

router = APIRouter(prefix="/questions", tags=["questions"])

@router.post("", response_model=QuestionOut, status_code=201)
def create_question(payload: QuestionCreate, db: Session = Depends(get_db)):
    q = Question(**payload.model_dump())
    db.add(q)
    db.commit()
    db.refresh(q)
    return q

@router.get("", response_model=list[QuestionOut])
def list_questions(
    tag: str | None = Query(default=None),
    difficulty: str | None = Query(default=None),
    limit: int = Query(default=50, ge=1, le=200),
    db: Session = Depends(get_db),
):
    stmt = select(Question).order_by(Question.created_at.desc()).limit(limit)
    if tag:
        stmt = stmt.where(Question.tag == tag)
    if difficulty:
        stmt = stmt.where(Question.difficulty == difficulty)

    results = db.execute(stmt).scalars().all()
    return results

@router.get("/{question_id}", response_model=QuestionOut)
def get_question(question_id: int, db: Session = Depends(get_db)):
    q = db.get(Question, question_id)
    if not q:
        raise HTTPException(status_code=404, detail="Question not found")
    return q
