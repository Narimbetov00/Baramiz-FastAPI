from fastapi import APIRouter,Depends
from .schemas import RouteCreateModel,RoutesModel,RouteUpdateModel
from fastapi.exceptions import HTTPException
from src.db.models import Routes
from typing import List
from src.api.v1.accounts.dependencies import get_current_user

routes_app = APIRouter()

@routes_app.get("/",response_model=List[RoutesModel])
async def get_all_routes():
    all_routes = await Routes.all()

    return list(all_routes)


@routes_app.post("/",response_model=RoutesModel)
async def add_route(route_data:RouteCreateModel,user=Depends(get_current_user)):
    if not user.is_verified:
        raise HTTPException(status_code=403,detail="Tastiyqlanbagan paydalaniwshilarga ruxsat joq!")
    new_route = await Routes.create(**route_data.dict())

    return new_route

@routes_app.get('/{route_id}',response_model=RoutesModel)
async def get_route(route_id:str):
    route = await Routes.get_or_none(id=route_id)
    if route:
        return route
    raise HTTPException(status_code=404,detail="Not Found")

@routes_app.put("/{route_id}",response_model=RoutesModel)
async def put_route(route_id:str,update_route_data:RouteUpdateModel,user=Depends(get_current_user)):
    if not user.is_verified:
        raise HTTPException(status_code=403,detail="Tastiyqlanbagan paydalaniwshilarga ruxsat joq!")
    route = await Routes.get_or_none(id=route_id)
    if not route:
        raise HTTPException(status_code=404,detail="Not Found")
    update_data = update_route_data.dict(exclude_unset=True)

    if update_data: 
        await route.update_from_dict(update_data)
        await route.save()

    return route

@routes_app.delete('/{route_id}',status_code=204)
async def delete_route(route_id:str,user=Depends(get_current_user)):
    if not user.is_verified:
        raise HTTPException(status_code=403,detail="Tastiyqlanbagan paydalaniwshilarga ruxsat joq!")
    route = await Routes.get_or_none(id=route_id)
    if not route:
        raise HTTPException(status_code=404,detail="Not Found")
    
    await route.delete()
    return {"message":"Successfully delete content"}