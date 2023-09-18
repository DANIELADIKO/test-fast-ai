from pydantic import BaseModel
from datetime import datetime


class ImageEntity(BaseModel):
    name: str
    link: str
    correctness: float
    category: str
    createdAt: datetime

    class Config:
        populate_by_name = True

