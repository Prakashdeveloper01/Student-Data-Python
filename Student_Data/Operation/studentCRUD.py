from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from typing import List, Optional
from Database.db import sessionLocal
from Module.modules import *

student_router = APIRouter()

def get_db():
    db = sessionLocal()  
    try:
        yield db
    finally:
        db.close()  

@student_router.get("/student", response_model=List[StudentResponse],tags=['Student'])
def read_students(db: Session = Depends(get_db)):
    try:
        return db.query(Student).all()
    except SQLAlchemyError as e:
        raise HTTPException(status_code=404, detail=f'Database not found: {str(e)}')

@student_router.post('/student', response_model=StudentResponse)
def create_student(student: UseStudent, db: Session = Depends(get_db)):
    try:
        new_student = Student(**student.dict())
        db.add(new_student)
        db.commit()
        db.refresh(new_student)
        return new_student
    except SQLAlchemyError as e:
        raise HTTPException(status_code=404, detail=f'Database not found: {str(e)}')

@student_router.put("/student/{student_id}", response_model=StudentResponse)
def update_student(student_id: int, name: Optional[str] = None, age: Optional[int] = None, db: Session = Depends(get_db)):
    try:
        student = db.query(Student).filter(Student.id == student_id).first()
        if not student:
            raise HTTPException(status_code=404, detail='Student not found')

        if name is not None:
            student.name = name
        if age is not None:
            student.age = age

        db.commit()
        return student
    except SQLAlchemyError as e:
        raise HTTPException(status_code=404, detail=f'Database not found: {str(e)}')

@student_router.delete("/student/{student_id}", response_model=StudentResponse)
def delete_student(student_id: int, db: Session = Depends(get_db)): 
    try:
        student = db.query(Student).filter(Student.id == student_id).first()
        if not student:
            raise HTTPException(status_code=404, detail='Student not found')
        db.delete(student)
        db.commit()
        return student
    except SQLAlchemyError as e:
        raise HTTPException(status_code=404, detail=f'Database not found: {str(e)}')
"""
@student_router.get("/student/{student_id}", response_model=StudentWithDetailsResponse)
def read_student_by_id(student_id: int, db: Session = Depends(get_db)):
    try:
        student = db.query(Student).filter(Student.id == student_id).first()
        if not student:
            raise HTTPException(status_code=404, detail='Student not found')

        student_details = db.query(StudentDetails).filter(StudentDetails.student_id == student_id).all()
        
        return StudentWithDetailsResponse(
            student=StudentResponse(id=student.id, name=student.name, age=student.age),
            details=[ResponseStudentDetails(
                SD_id=detail.SD_id,
                student_id=detail.student_id,
                qualification=detail.qualification,
                address=detail.address
            ) for detail in student_details]
        )
    except SQLAlchemyError as e:
        raise HTTPException(status_code=404, detail=f'Database not found: {str(e)}')
"""

@student_router.get("/student/full/{student_id}", response_model=Combine)
async def get_student_full_details(student_id: int, db: Session = Depends(get_db)):
    return await full_Response_details(student_id, db)
