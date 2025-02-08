from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
import time
import logging 
logger = logging.getLogger("uvicorn.access")
logger.disabled = True


def register_middleware(app:FastAPI):

    app.add_middleware(CORSMiddleware,
                       allow_origins=["*"],
                        allow_methods=["*"],
                        allow_headers=["*"] ,
                        allow_credentials=True)
    
    app.add_middleware(TrustedHostMiddleware,
                       allowed_hosts=["baramiz-fastapi.onrender.com"])
        