from fastapi import FastAPI, Depends, HTTPException
from typing_extensions import Annotated, List
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import engine, SessionLocal
from fastapi.middleware.cors import CORSMiddleware
import models
import uvicorn

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
    description: str
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

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.post("/posts_blog/", response_model=UserModel)
async def create_post(posts_blog: UserBase, db: db_dependency):
    db_post = models.User(**posts_blog.dict()) 
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post


@app.get("/posts_blog/", response_model=List[UserModel])
async def read_posts_blog(db: db_dependency, skip: int = 0, limit: int = 100):
    posts = db.query(models.User).offset(skip).limit(limit).all()
    return posts

@app.get("/posts_blog/{post_id}", response_model=UserModel)
async def read_post_blog_by_id(post_id: int, db: db_dependency):
    post = db.query(models.User).filter(models.User.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post


@app.put("/posts_blog/{post_id}")
async def update_post_blog_by_id(post_id: int, post: UserBase, db: db_dependency):
    db_post = db.query(models.User).filter(models.User.id == post_id).first()
    if not db_post:
        raise HTTPException(status_code=404, detail="Post not found")
    db_post.title = post.title
    db_post.content = post.content
    db_post.description = post.description
    db_post.date = post.date
    db.commit()
    db.refresh(db_post)
    return db_post

@app.delete("/posts_blog/{post_id}")
async def delete_post_blog_by_id(post_id: int, db: db_dependency):
    post = db.query(models.User).filter(models.User.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    db.delete(post)
    db.commit()
    return {"message": "Post deleted"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)