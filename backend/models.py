from database import Base
from sqlalchemy import Column, Integer, String, Boolean

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    content = Column(String)
    description = Column(String)
    is_active = Column(Boolean)
    date = Column(String)