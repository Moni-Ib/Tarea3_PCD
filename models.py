from sqlalchemy import Column, Integer, String, JSON
from database import Base

class Users(Base):
    __tablename__ = "users"

    user_name = Column(String)
    user_id = Column(Integer, primary_key=True, index=True)
    user_email = Column(String)
    age = Column(Integer)
    recommendations = Column(JSON)
    ZIP = Column(String)