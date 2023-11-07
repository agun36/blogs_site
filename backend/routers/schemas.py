from pydantic import BaseModel
from datetime import datetime


class PostBase(BaseModel):
	title: str
	author: str
	content: str


class PostDisplay(PostBase):
	id: int
	timestamp: datetime

	class Config:
		orm_mode = True
