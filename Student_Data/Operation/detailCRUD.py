from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from typing import List, Optional

from Database.db import sessionLocal
from Module.modules import * 

detail_router = APIRouter()

def get_db():
    db = sessionLocal()  
    try:
        yield db
    finally:
        db.close() 

# CRUD for StudentDetails
# Create a New Student Details
@detail_router.post('/studentdetails', response_model=ResponseStudentDetails)
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
@detail_router.get("/studentdetails", response_model=List[ResponseStudentDetails])
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
@detail_router.delete("/studentdetails/{detail_id}", response_model=ResponseStudentDetails)
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
@detail_router.put("/studentdetails/{detail_id}", response_model=ResponseStudentDetails)
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
@detail_router.get("/studentdetails/{detail_id}", response_model=ResponseStudentDetails)
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
        
        
