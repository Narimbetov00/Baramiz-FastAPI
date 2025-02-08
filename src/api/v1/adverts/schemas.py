from pydantic import BaseModel
import uuid
from datetime import datetime
from urllib.parse import urljoin
from src.config import Config

BASE_URL = f"http://{Config.DOMAIN}"

class AdvertModel(BaseModel):
    id: uuid.UUID
    title: str
    description: str
    link: str
    file: str
    date: datetime

    def dict(self, *args, **kwargs):
        result = super().dict(*args, **kwargs)
        result["file"] = urljoin(BASE_URL, result["file"])
        return result
    

class AdvertUpdateModel(BaseModel):
    title: str | None = None
    description: str | None = None
    link: str | None = None