from fastapi import FastAPI
from .routers import user, course
from .database import engine, Base
from . import models

# Auto create tables on startup
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(course.router)
app.include_router(user.router)
app.include_router(course.courses_router)