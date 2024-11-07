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

@student_router.get("/student", response_model=List[StudentResponse])
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
    
    finally:
        db.close()
    
    
@student_router.get("/student/{student_id}",response_model=StudentResponse)
async def get_student_by_id(student_id : int , db:Session = Depends(get_db)):
    try :
        student = db.query(Student).filter(Student.id == student_id).first()
        if not student:
            raise HTTPException(status_code=404,detail='Student not found')
        return student
    
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=404,detail='Database not found')
    
    finally:
        db.close()