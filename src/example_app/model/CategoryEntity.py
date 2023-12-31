from pydantic import BaseModel, Field
from datetime import datetime

class CategoryEntity(BaseModel):
    name: str
    createdAt: datetime

    class Config:
        populate_by_name = True
