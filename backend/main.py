from fastapi import FastAPI, Depends, HTTPException
from typing import Annotated
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import engine, SessionLocal
import models
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    'http://localhost:3000',
]

app.add_middleware(
    CORSMiddleware, 
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class UserBase(BaseModel):
    title: str
    content: str
    decription: str
    is_active: bool
    date: str


class UserModel(UserBase):
    id: int


    class config:
        orm_mode = True


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
models.Base.metadata.create_all(bind=engine) 

@app.post("/posts_blog/", response_model=UserModel)
async def create_post(db: db_dependency, post: UserBase):
    db_post = models.User(**post.dict()) 
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post