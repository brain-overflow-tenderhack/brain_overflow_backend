from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.routers import *

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "PATCH", "DELETE", "PUT"],
    allow_headers=["*"],
)

app.include_router(session_router)


# @app.on_event("startup")
# async def startup(): ...
#
#
# @app.on_event("shutdown")
# async def shutdown(): ...
