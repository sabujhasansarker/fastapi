from fastapi import Depends, HTTPException,status, APIRouter
from sqlalchemy.orm import Session
from .. import models
from ..schemas import UserCreate, UserResponse
from ..database import  get_db
from .. import utils


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

# create user
@router.post("/user",status_code=status.HTTP_201_CREATED, response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)) :
    if db.query(models.User).filter(models.User.email == user.email).first() :
        raise HTTPException(400, "Email already exits")
    hashed_password = utils.hash_password(user.password)
    user.password = hashed_password
    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user