from fastapi import APIRouter, Depends,UploadFile,File,Form
from .schemas import AdvertModel
from fastapi.exceptions import HTTPException
from src.db.models import Adverts
from src.api.v1.accounts.dependencies import get_current_user
from typing import List
from src.config import Config
import os
import shutil
import uuid
advert_route = APIRouter()

BASE_URL = Config.DOMAIN

def add_base_url_to_file(advert):
    advert["file"] = f"http://{BASE_URL}/{advert['file']}"
    return advert

MEDIA_FOLDER = "media"
os.makedirs(MEDIA_FOLDER, exist_ok=True)

@advert_route.post('/',response_model=AdvertModel)
async def add_advert(title: str, description: str, link: str,file:UploadFile=File(...),user=Depends(get_current_user)):
    if not user.is_verified:
        raise HTTPException(status_code=403,detail="Tastiyqlanbagan paydalaniwshilarga ruxsat joq!")
    unique_filename = f"{uuid.uuid4()}-{file.filename}"
    file_path = f"{MEDIA_FOLDER}/{unique_filename}"
   
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    advert = await Adverts.create(
        title=title,
        description=description,
        link=link,
        file=file_path
    )
    return map(add_base_url_to_file, advert)


@advert_route.get("/",response_model=List[AdvertModel])
async def get_all_adverts():
    adverts = await Adverts.all().values()

    return list(map(add_base_url_to_file, adverts))



@advert_route.get('/{advert_id}',response_model=AdvertModel)
async def get_advert(advert_id:str):
    advert = await Adverts.get_or_none(id=advert_id)
    if advert:
        return map(add_base_url_to_file, advert)
    raise HTTPException(status_code=404,detail="Not Found")

@advert_route.put("/{advert_id}",response_model=AdvertModel)
async def put_advert(advert_id:str,title: str = Form(None),
    description: str = Form(None),
    link: str = Form(None),file:UploadFile=None,user=Depends(get_current_user)):
    if not user.is_verified:
        raise HTTPException(status_code=403,detail="Tastiyqlanbagan paydalaniwshilarga ruxsat joq!")
    advert = await Adverts.get_or_none(id=advert_id)
    if not advert:
        raise HTTPException(status_code=404,detail="Not Found")
    
  
    if title:
        advert.title = title
    if description:
        advert.description = description
    if link:
        advert.link = link

    if file:
        file_path = f"media/{file.filename}"
        with open(file_path, "wb") as f:
            f.write(file.file.read())
        advert.file = file_path

    await advert.save()

    return {
        "id": advert.id,
        "title": advert.title,
        "description": advert.description,
        "link": advert.link,
        "file": f"http://{Config.DOMAIN}/{advert.file}",
        "date": advert.date
    }
 
@advert_route.delete('/{advert_id}',status_code=204)
async def delete_advert(advert_id:str,user=Depends(get_current_user)):
    if not user.is_verified:
        raise HTTPException(status_code=403,detail="Tastiyqlanbagan paydalaniwshilarga ruxsat joq!")
    advert = await Adverts.get_or_none(id=advert_id)
    if not advert:
        raise HTTPException(status_code=404,detail="Not Found")
    
    await advert.delete()
    return {"message":"Successfully delete content"}