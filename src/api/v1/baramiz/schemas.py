from pydantic import BaseModel,Field
import uuid
from datetime import datetime
from typing import Optional

class RoutesModel(BaseModel):
    id:uuid.UUID
    from_dan:str
    to_ga:str
    number:int
    description:str
    created_at:datetime
    updated_at:datetime

class RouteCreateModel(BaseModel):
    from_dan:str=Field(max_length=255)
    to_ga:str=Field(max_length=255)
    number:int
    description:str

class RouteUpdateModel(BaseModel):
    from_dan: Optional[str] = None
    to_ga: Optional[str] = None
    number: Optional[int] = None
    description: Optional[str] = None

