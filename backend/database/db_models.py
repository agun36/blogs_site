from .db_setup import Base
from sqlalchemy import Column, DateTime, Integer, String

class DbArticle(Base):
	__tablename__ = "post"
	id = Column(Integer, primary_key=True, index=True)
	title = Column(String)
	content = Column(String)
	author = Column(String)
	timestamp = Column(DateTime)