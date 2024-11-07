from pydantic import BaseModel
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Integer, Column, String, ForeignKey
from typing import Optional , List

Base = declarative_base()

class Student(Base):
    __tablename__ = 'student'  

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)

    student_details = relationship('StudentDetails', back_populates='student')
    student_marks = relationship('mark', back_populates='student')

class UseStudent(BaseModel):
    name: str
    age: int

class StudentResponse(UseStudent):
    id: int
    
    class Config:
        from_attributes =True