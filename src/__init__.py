from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
from src.api.v1.accounts.routes import auth_router
from src.api.v1.baramiz.routes import routes_app
from src.api.v1.reviews.routes import review_route
from src.api.v1.adverts.routes import advert_route
from src.db.main import init_db,close_db
from .middleware import register_middleware

v1 = "v1"

app = FastAPI(title="Baramiz",
              description="A Rest API For a Baramiz Review web service",
              version=v1,
              docs_url=f"/api/{v1}/docs",
              redoc_url=f"/api/{v1}/redoc")


@app.on_event("startup")
async def startup():
    await init_db()

@app.on_event("shutdown")
async def shutdown():
    await close_db()

@app.get("/",tags=["Baramiz API"])
async def view():
    return {"message":"Welcome to Baramiz OPEN API View"}

import os

MEDIA_FOLDER = "media"
os.makedirs(MEDIA_FOLDER, exist_ok=True)


register_middleware(app)

app.mount("/media", StaticFiles(directory=MEDIA_FOLDER), name="media")
app.include_router(auth_router,prefix=f"/api/{v1}/auth",tags=["Auth"])
app.include_router(routes_app,prefix=f"/api/{v1}/routes",tags=["Routes"])
app.include_router(review_route,prefix=f"/api/{v1}/reviews",tags=["Reviews"])
app.include_router(advert_route,prefix=f"/api/{v1}/adverts",tags=["Adverts"])

