from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .route import router
from src.domain_error import DomainError
from .error_handler import domain_error_handler, global_error_handler

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,  # MUST be False when using "*"
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(router)
app.add_exception_handler(DomainError, domain_error_handler)
app.add_exception_handler(Exception, global_error_handler)