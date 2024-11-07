from pydantic import BaseModel
from fastapi import HTTPException
from sqlalchemy.orm import declarative_base, relationship , Session
from sqlalchemy import Integer, Column, String, ForeignKey
from typing import Optional , List
from Module.details import *
from Module.student import *

Base = declarative_base()

class Student(Base):
    __tablename__ = 'student'  

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)

    student_details = relationship('StudentDetails', back_populates='student',uselist= False)
    student_marks = relationship('Mark', back_populates='student')

class UseStudent(BaseModel):
    name: str
    age: int

class StudentResponse(UseStudent):
    id: int
    
    class Config:
        from_attributes =True
        

class StudentDetails(Base):
    __tablename__ = 'students_details'  

    SD_id = Column(Integer, primary_key=True)
    qualification = Column(String, nullable=False)
    address = Column(String, nullable=False)
    student_id = Column(Integer, ForeignKey('student.id'))  

    student = relationship('Student', back_populates='student_details')

class UseStudentDetail(BaseModel):
    qualification: Optional[str]
    address: Optional[str]
    student_id: Optional[int]

class ResponseStudentDetails(UseStudentDetail):
    SD_id: int
    
    class Config:
        from_attributes = True


class StudentWithDetailsResponse(BaseModel):
    student: StudentResponse
    details: List[ResponseStudentDetails]
    

class Mark(Base):
    __tablename__ = 'mark'  

    id = Column(Integer, primary_key=True)
    tamil = Column(Integer, nullable=False)
    english = Column(Integer, nullable=False)
    maths = Column(Integer, nullable=False)
    science = Column(Integer, nullable=False)
    social = Column(Integer, nullable=False)
    student_id = Column(Integer, ForeignKey('student.id'))

    student = relationship('Student', back_populates='student_marks')
    

class UseMark(BaseModel):
    tamil: int
    english : int
    maths: int
    science: int
    social : int
    student_id: Optional[int]

class MarkResponse(UseMark):
    id: int
    
    class Config:
        from_attributes =True


# Combine Class 
class Combine(BaseModel):
    name: str
    age: int
    qualification: Optional[str] = None
    address: Optional[str] = None
    student_id: int
    marks : List[UseMark]