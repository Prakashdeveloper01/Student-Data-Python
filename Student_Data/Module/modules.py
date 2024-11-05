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

    details = relationship('StudentDetails', back_populates='student')
    marks = relationship('Mark', back_populates='student')

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
    

class Mark(Base):
    __tablename__ = 'mark'  

    id = Column(Integer, primary_key=True)
    tamil = Column(Integer, nullable=False)
    english = Column(Integer, nullable=False)
    maths = Column(Integer, nullable=False)
    science = Column(Integer, nullable=False)
    social = Column(Integer, nullable=False)
    student_id = Column(Integer, ForeignKey('student.id'))

    student = relationship('Student', back_populates='marks')

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
    qualification: Optional[str]
    address: Optional[str]
    student_id: int
    marks : List[UseMark]

async def full_Response_details(student_id: int, db: Session) -> Combine:
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail='Student not found')

    details = db.query(StudentDetails).filter(StudentDetails.student_id == student_id).first()
    marks = db.query(Mark).filter(Mark.student_id == student_id).first()
    marks_list = []
    if marks:
        marks_list.append(UseMark(
            tamil=marks.tamil,
            english=marks.english,
            maths=marks.maths,
            science=marks.science,
            social=marks.social,
            student_id=marks.student_id
        ))

    combine_response = Combine(
        name=student.name,
        age=student.age,
        qualification=details.qualification if details else None,
        address=details.address if details else None,
        student_id=student.id,
        marks=marks_list 
    )

    return combine_response
