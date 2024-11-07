from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from Database.db import sessionLocal
from Module.modules import *
from Module.combine import *

full_router = APIRouter()

def get_db():
    db = sessionLocal()  
    try:
        yield db
    finally:
        db.close()

# Read the Student Full Details
@full_router.get("/student/full/{student_id}", response_model=Combine)
async def get_student_full_details(student_id: int, db: Session = Depends(get_db)):
    return await full_Response_details(student_id, db)

#Create a New Student Full Details
@full_router.post('/student/full', response_model=Combine)
def create_student(
    name: str, 
    age: int, 
    qualification: str = None, 
    address: str = None, 
    marks: List[UseMark] = None, 
    db: Session = Depends(get_db)
):
    # Create student
    student = Student(name=name, age=age)
    db.add(student)
    db.commit()
    
    # Create student details
    new_details = StudentDetails(student_id=student.id, qualification=qualification, address=address)
    db.add(new_details)
    db.commit()
    
    marks_list = []
    for mark in marks:
        student_marks = Mark(
            student_id=student.id,
            tamil=mark.tamil,
            english=mark.english,
            maths=mark.maths,
            science=mark.science,
            social=mark.social
        )
        db.add(student_marks)
        db.commit()
        db.refresh(student_marks)

        marks_list.append(UseMark(
            tamil=student_marks.tamil,
            english=student_marks.english,
            maths=student_marks.maths,
            science=student_marks.science,
            social=student_marks.social,
            student_id=student_marks.student_id
        ))

    details = db.query(StudentDetails).filter(StudentDetails.student_id == student.id).first()
    marks_db = db.query(Mark).filter(Mark.student_id == student.id).all()

    combine_response = Combine(
        name=student.name,
        age=student.age,
        qualification=details.qualification if details else None,
        address=details.address if details else None,
        student_id=student.id,
        marks=marks_list  
    )

    return combine_response


# Update the Student Full Details
@full_router.put('/student/full/{student_id}', response_model=Combine)
def update_student(
    student_id: int,  
    name: str = None, 
    age: int = None, 
    qualification: str = None, 
    address: str = None, 
    marks: List[UseMark] = None, 
    db: Session = Depends(get_db)
):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    if name is not None:
        student.name = name
    if age is not None:
        student.age = age

    details = db.query(StudentDetails).filter(StudentDetails.student_id == student_id).first()
    if details:
        if qualification is not None:
            details.qualification = qualification
        if address is not None:
            details.address = address
        
    else:
        new_details = StudentDetails(
            student_id=student.id,
            qualification=qualification,
            address=address
        )
        db.add(new_details)

    if marks is not None:
        
        db.query(Mark).filter(Mark.student_id == student_id).delete()

        
        for mark in marks:
            student_marks = Mark(
                student_id=student.id,
                tamil=mark.tamil,
                english=mark.english,
                maths=mark.maths,
                science=mark.science,
                social=mark.social
            )
            db.add(student_marks)
            db.commit()

    updated_details = db.query(StudentDetails).filter(StudentDetails.student_id == student.id).first()
    updated_marks = db.query(Mark).filter(Mark.student_id == student.id).all()

    marks_list = [
        UseMark(
            tamil=mark.tamil,
            english=mark.english,
            maths=mark.maths,
            science=mark.science,
            social=mark.social,
            student_id=mark.student_id
        ) for mark in updated_marks
    ]

    combine_response = Combine(
        name=student.name,
        age=student.age,
        qualification=updated_details.qualification if updated_details else None,
        address=updated_details.address if updated_details else None,
        student_id=student.id,
        marks=marks_list  
    )

    return combine_response
