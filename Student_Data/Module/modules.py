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

    details = relationship('StudentDetails', back_populates='student')

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

    student = relationship('Student', back_populates='details')

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
    
class WriteResponse(BaseModel):
    Response : List[StudentWithDetailsResponse]