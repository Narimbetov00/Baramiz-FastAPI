from fastapi import APIRouter, Depends
from .schemas import ReviewsModel,ReviewsCreateModel
from fastapi.exceptions import HTTPException
from src.db.models import Reviews
from src.api.v1.accounts.dependencies import get_current_user
from typing import List

review_route = APIRouter()


@review_route.get('/',response_model=List[ReviewsModel])
async def get_all_reviews():
    reviews = await Reviews.all()
    return list(reviews)

@review_route.post('/',response_model=ReviewsModel)
async def add_review(review_data:ReviewsCreateModel,user=Depends(get_current_user)):
    if not user:
        raise HTTPException(status_code=403,detail="Loginnen otin!")
    
    new_review = await Reviews.create(**review_data.dict())

    return new_review

@review_route.delete('/{review_id}',status_code=204)
async def delete_review(review_id:str,user=Depends(get_current_user)):
    if not user.is_verified:
        raise HTTPException(status_code=403,detail="Tastiyqlanbagan paydalaniwshilarga ruxsat joq!")
    
    route = await Reviews.get_or_none(id=review_id)
    if not route:
        raise HTTPException(status_code=404,detail="Not Found")
    
    await route.delete()
    return {"message":"Successfully delete content"}

