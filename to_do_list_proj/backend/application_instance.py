from starlette.middleware.cors import CORSMiddleware
from fastapi import FastAPI

from router_auth import router_auth
from create_app_endpoints import router_main

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
    
app.include_router(router_auth,prefix="/api" )
app.include_router(router_main, prefix="/api")
