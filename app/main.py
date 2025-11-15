from fastapi import FastAPI, Depends, HTTPException,status,Response
from sqlalchemy.orm import Session
from . import models
from .schemas import CourseResponse, CourseCreate
from .database import engine, get_db

# Create tables
models.Base.metadata.create_all(bind=engine)
app = FastAPI()

# Root endpoint
@app.get("/")
def root(db: Session = Depends(get_db)):
    return {"status": "SQLAlchemy ORM working"}

# Add course
@app.post('/course', response_model=CourseResponse)
def create_course(course: CourseCreate, db: Session = Depends(get_db)):
    new_course = models.Course(**course.model_dump())
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
@app.get("/course/{id}",response_model=CourseResponse)
def get_course(id:int,db: Session = Depends(get_db)):
    course= db.query(models.Course).filter(models.Course.id == id).first()
    if not course:
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail=f"course not found id:{id}"
        )
    return course

#edit data
@app.put("/course/{id}",response_model=CourseResponse)
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
     return course

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
