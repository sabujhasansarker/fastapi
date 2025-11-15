
from pydantic import BaseModel, field_validator, ConfigDict, EmailStr
from typing import Optional
from datetime import datetime

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

# user create
class UserCreate(BaseModel):
    email : EmailStr
    password : str

# get user
class UserResponse(BaseModel):
    id: int
    email : EmailStr
    created_at : datetime

    class Config:
        orrm_model = True