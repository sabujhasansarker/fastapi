from fastapi import FastAPI
from .routers import user, course
from .database import engine, Base
from . import models
from fastapi.middleware.cors import CORSMiddleware

# Auto create tables on startup
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000","https://*.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(course.router)
app.include_router(user.router)
app.include_router(course.courses_router)