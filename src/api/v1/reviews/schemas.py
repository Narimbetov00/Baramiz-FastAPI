from pydantic import BaseModel,Field
import uuid
from datetime import datetime



class ReviewsModel(BaseModel):
    id :uuid.UUID
    rating:int
    text:str
    created_at:datetime

class ReviewsCreateModel(BaseModel):
    rating:int=Field(ge=1,le=5)
    text:str


