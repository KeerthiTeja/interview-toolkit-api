from fastapi import FastAPI

from app.db.session import engine
from app.db.base import Base
from app.db import models  # noqa: F401

from app.api.routes_questions import router as questions_router
from app.api.routes_sessions import router as sessions_router
from app.core.logging import setup_logging, request_id_middleware

# Setup logging first
setup_logging()

# Create tables
Base.metadata.create_all(bind=engine)

# Create ONE FastAPI app
app = FastAPI(title="Interview Toolkit API", version="0.1.0")

# Middleware
app.middleware("http")(request_id_middleware)

# Routes
@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/")
def root():
    return {"service": "Interview Toolkit API", "status": "ok", "docs": "/docs"}

# Include routers
app.include_router(questions_router)
app.include_router(sessions_router)
