from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from typing import List, Optional

from Database.db import sessionLocal
from Module.modules import * 
#(
    #StudentDetails, 
    #Student, 
    #StudentResponse, 
    #UseStudent, 
    #ResponseStudentDetails, 
    #UseStudentDetail,
    #StudentWithDetailsResponse, WriteResponse
#)

app = FastAPI()

def get_db():
    db = sessionLocal()  
    try:
        yield db
    finally:
        db.close()  

# Read all students in database
@app.get("/student", response_model=List[StudentResponse])
def read_students(db: Session = Depends(get_db)):
    try:
        students = db.query(Student).all()
        return students
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException (status_code= 404 , detail='Database not found {e}')
    finally:
        db.close()

# Create a new Student
@app.post('/student', response_model=StudentResponse)
def create_student(student: UseStudent, db: Session = Depends(get_db)):
    try:
        new_student = Student(**student.dict())
        db.add(new_student)
        db.commit()
        db.refresh(new_student)
        return new_student
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException (status_code= 404 , detail='Database not fond {e}')
    finally:
        db.close()

# Update a Exisiting Student
@app.put("/student/{student_id}", response_model=StudentResponse)
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
    
    except SQLAlchemyError as e :
        db.rollback()
        raise HTTPException (status_code= 404 , detail= ' Database not found{e}')
    
    finally:
        db.close()

#Delete a Student by id
@app.delete("/student/{student_id}", response_model=StudentResponse)
def delete_student(student_id: int, db: Session = Depends(get_db)): 
    try:
        student = db.query(Student).filter(Student.id == student_id).first()
        if not student:
            raise HTTPException(status_code=404, detail='Student not found')
        db.delete(student)
        db.commit()
        return student
    
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException (status_code= 404 , detail='Database not found {e}')
    
    finally:
        db.close()

# Get student by id
@app.get("/student/{student_id}", response_model=StudentWithDetailsResponse)
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
    # return WriteResponse
    
    except SQLAlchemyError as e :
        db.rollback()
        raise HTTPException ( status_code=404 , detail='Database not found {e}')
    
    finally:
        db.close()


# CRUD for StudentDetails
# Create a New Student Details
@app.post('/studentdetails', response_model=ResponseStudentDetails)
def create_student_details(detail: UseStudentDetail, db: Session = Depends(get_db)):
    try:
        new_detail = StudentDetails(**detail.dict())
        db.add(new_detail)
        db.commit()
        db.refresh(new_detail)
        return ResponseStudentDetails(SD_id=new_detail.SD_id, qualification=new_detail.qualification,
                                    address=new_detail.address, student_id=new_detail.student_id)
        
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException( status_code=404 , detail='Database not found{e}')
    
    finally:
        db.close()

# Read all the Student Details
@app.get("/studentdetails", response_model=List[ResponseStudentDetails])
def read_student_details(db: Session = Depends(get_db)):
    try:
        details = db.query(StudentDetails).all()
        return details
    
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException (status_code= 404 , detail='Database not found{e}')
    
    finally:
        db.close()

#Delete a Student Details by id
@app.delete("/studentdetails/{detail_id}", response_model=ResponseStudentDetails)
def delete_student_details(detail_id: int, db: Session = Depends(get_db)): 
    try:
        detail = db.query(StudentDetails).filter(StudentDetails.SD_id == detail_id).first()

        if not detail:
            raise HTTPException(status_code=404, detail='Student detail not found')

        db.delete(detail)
        db.commit()

        return ResponseStudentDetails(
            SD_id=detail.SD_id,
            student_id=detail.student_id,
            qualification=detail.qualification,
            address=detail.address
        )
        
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code= 404 , detail='Database not found{e}')
    
    finally:
        db.close()

# Update the Student Details
@app.put("/studentdetails/{detail_id}", response_model=ResponseStudentDetails)
def update_student_details(detail_id: int, qualification: Optional[str] = None, address: Optional[str] = None, 
                           student_id: Optional[int] = None, db: Session = Depends(get_db)):
    try:
        detail = db.query(StudentDetails).filter(StudentDetails.SD_id == detail_id).first()
        if not detail:
            raise HTTPException(status_code=404, detail='Student detail not found')

        if qualification is not None:
            detail.qualification = qualification
        if address is not None:
            detail.address = address
        if student_id is not None:
            detail.student_id = student_id

        db.commit()
        db.refresh(detail)
        return ResponseStudentDetails(
            SD_id=detail.SD_id,
            student_id=detail.student_id,
            qualification=detail.qualification,
            address=detail.address
        )
        
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code= 404 , detail='Database not found{e}')
    
    finally:
        db.close()

# Read the Student Details by id
@app.get("/studentdetails/{detail_id}", response_model=ResponseStudentDetails)
def read_student_details_by_id(detail_id: int, db: Session = Depends(get_db)):
    try:
        detail = db.query(StudentDetails).filter(StudentDetails.SD_id == detail_id).first()
        if not detail:
            raise HTTPException(status_code=404, detail='Student detail not found')
        return ResponseStudentDetails(SD_id=detail.SD_id, student_id=detail.student_id, qualification=detail.qualification, address=detail.address)
    
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException ( status_code= 404, detail='Database not found{e}')
    
    finally:
        db.close()