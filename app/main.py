from fastapi import FastAPI, Depends, HTTPException,status,Response
from pydantic import BaseModel, field_validator, ConfigDict
from typing import Optional
from sqlalchemy.orm import Session
from . import models
from .database import engine, get_db

# Create tables
models.Base.metadata.create_all(bind=engine)
app = FastAPI()

# Request Schema
class CourseCreate(BaseModel):
    name: str
    instructor: str
    duration: float
    website: Optional[str] = None

    @field_validator('website', mode='before')
    @classmethod
    def validate_website(cls, v):
        if v == '' or v is None:
            return None
        if v and not v.startswith(('http://', 'https://')):
            return f'https://{v}'
        return v


# Response Schema
class CourseResponse(BaseModel):
    id: int
    name: str
    instructor: str
    duration: float
    website: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

# Root endpoint
@app.get("/")
def root(db: Session = Depends(get_db)):
    return {"status": "SQLAlchemy ORM working"}

# Add course
@app.post('/courses', response_model=CourseResponse)
def create_course(course: CourseCreate, db: Session = Depends(get_db)):
    new_course = models.Course(
        name=course.name,
        instructor=course.instructor,
        duration=course.duration,
        website=course.website,
    )
    db.add(new_course)
    db.commit()
    db.refresh(new_course)
    return new_course

# Get all courses
@app.get("/courses", response_model=list[CourseResponse])
def get_courses(db: Session = Depends(get_db)):
    courses = db.query(models.Course).all()
    return courses

# get with id
@app.get("/course/{id}")
def get_course(id:int,db: Session = Depends(get_db)):
    course= db.query(models.Course).filter(models.Course.id == id).first()
    if not course:
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail=f"course not found id:{id}"
        )
    return {"course":course}

#edit data
@app.put("/course/{id}")
def update_course(id:int,update_course: CourseCreate,db: Session = Depends(get_db)):
     course_query= db.query(models.Course).filter(models.Course.id == id)
     course = course_query.first()
     if not course:
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail=f"course not found id:{id}"
        )
     update_data = update_course.model_dump()
     course_query.update(update_data,synchronize_session=False)
     db.commit()
     db.refresh(course)
     return{"updated course":course}

# delete data
@app.delete("/course/{id}",status_code=status.HTTP_204_NO_CONTENT)
def get_course(id:int,db: Session = Depends(get_db)):
    course_query= db.query(models.Course).filter(models.Course.id == id)
    course= course_query.first()
    if not course:
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail=f"course not found id:{id}"
        )
    course_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
