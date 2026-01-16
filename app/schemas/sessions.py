from datetime import datetime
from pydantic import BaseModel
from typing import List

class SessionCreate(BaseModel):
    tag: str | None = None
    difficulty: str | None = None
    count: int = 5


from pydantic import BaseModel, ConfigDict

class SessionOut(BaseModel):
    id: int
    created_at: datetime
    question_ids: List[int]

    model_config = ConfigDict(from_attributes=True)
