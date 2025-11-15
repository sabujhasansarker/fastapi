from fastapi import FastAPI, Depends
from sqlalchemy.orm import  Session
from . import models
from . database import engine, get_db

# Create tables
models.Base.metadata.create_all(bind=engine)
app = FastAPI()

@app.get("/")
def course(db: Session = Depends(get_db)):
    return {"status": "SQLAlchemy ORM working"}
