from pydantic import BaseModel
from fastapi import HTTPException
from sqlalchemy.orm import declarative_base, relationship , Session
from sqlalchemy import Integer, Column, String, ForeignKey

Base = declarative_base()

class Mark(Base):
    __tablename__ = 'mark'  

    id = Column(Integer, primary_key=True)
    tamil = Column(Integer, nullable=False)
    english = Column(Integer, nullable=False)
    maths = Column(Integer, nullable=False)
    science = Column(Integer, nullable=False)
    social = Column(Integer, nullable=False)
    
    
    student = relationship('Student', back_populates='marks')

class UseMark(BaseModel):
    id : int
    tamil: int
    english : int
    maths: int
    science: int
    social : int

class MarkResponse(UseMark):
    id: int
    
    class Config:
        from_attributes =True
        