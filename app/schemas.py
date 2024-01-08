from pydantic import BaseModel, EmailStr
from pydantic.types import conint
from datetime import datetime
from typing import Optional


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True
    
    
   
    


class CreatePost(PostBase):
  pass


class UpdatePost(PostBase):
   pass

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True

class PostResponse(PostBase):
    id: int
    owner_id: int
    created_at: datetime
    owner: UserResponse


class UserCreate(BaseModel):
    email: EmailStr
    password: str





class GetUser(BaseModel):
    id: int
    email: EmailStr
    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str
    class Config:
        orm_mode = True



class Token(BaseModel):
    access_token: str
    token_type: str
    class Config:
        orm_mode = True

class TokenData(BaseModel):
    id: int
    class Config:
        orm_mode = True


class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)



class VoteOut(BaseModel):
    Post: PostResponse
    vote: int
    class Config:
        orm_mode = True