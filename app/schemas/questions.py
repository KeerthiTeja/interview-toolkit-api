from datetime import datetime
from pydantic import BaseModel, Field

class QuestionCreate(BaseModel):
    title: str = Field(min_length=3, max_length=200)
    body: str = Field(min_length=3)
    tag: str = Field(min_length=1, max_length=50)
    difficulty: str = Field(pattern="^(easy|medium|hard)$")

from pydantic import BaseModel, ConfigDict

class QuestionOut(BaseModel):
    id: int
    title: str
    body: str
    tag: str
    difficulty: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

