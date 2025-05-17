from starlette.middleware.cors import CORSMiddleware
from fastapi import FastAPI

from router_auth import router_auth
from create_app_endpoints import create_app_endpoints

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
    
app.include_router(router_auth)
create_app_endpoints(app)