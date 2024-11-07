from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from typing import List, Optional

from Database.db import sessionLocal
from Module.modules import * 

mark_router = APIRouter()

def get_db():
    db = sessionLocal()  
    try:
        yield db
    finally:
        db.close() 

# Create a New Mark
@mark_router.post('/mark', response_model=MarkResponse)
def create_mark(mark: UseMark, db: Session = Depends(get_db)):
    try:
        new_mark = Mark(**mark.dict())  
        db.add(new_mark)
        db.commit()
        db.refresh(new_mark)
        
        return MarkResponse(
            id=new_mark.id,  
            tamil=new_mark.tamil,
            english=new_mark.english,  
            maths=new_mark.maths,
            science=new_mark.science,
            social=new_mark.social,
            student_id=new_mark.student_id
        )
        
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=404, detail=f'Database not found')  
    
    finally:
        db.close()
        
        

# Read all the mark
@mark_router.get("/mark", response_model=List[MarkResponse])
def read_mark(db: Session = Depends(get_db)):
    try:
        marks = db.query(Mark).all()
        return marks
    
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException (status_code= 404 , detail='Database not found{e}')
    
    finally:
        db.close()


#Delete a Mark by id
@mark_router.delete("/mark/{mark_id}", response_model=MarkResponse)
def delete_mark(mark_id: int, db: Session = Depends(get_db)): 
    try:
        marks = db.query(Mark).filter(Mark.id == mark_id).first()

        if not marks:
            raise HTTPException(status_code=404, detail='Mark detail not found')

        db.delete(marks)
        db.commit()

        return marks
        
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code= 404 , detail='Database not found{e}')
    
    finally:
        db.close()
        

# Update the Student Details
@mark_router.put("/mark/{detail_id}", response_model=MarkResponse)
def update_mark(mark_id: int, tamil : Optional[int],english : Optional[int],maths:Optional[int],science:Optional[int],social : Optional[int], 
                           student_id: Optional[int] = None, db: Session = Depends(get_db)):
    try:
        marks = db.query(Mark).filter(Mark.id == mark_id).first()
        if not marks:
            raise HTTPException(status_code=404, detail='Student detail not found')

        if tamil is not None:
            marks.tamil = tamil
        if english is not None:
            marks.english = english
        if maths is not None:
            marks.maths = maths
        if science is not None:
            marks.science = science
        if social is not None:
            marks.social = social
        if student_id is not None:
            marks.student_id = student_id

        db.commit()
        db.refresh(marks)
        return MarkResponse(
            id=marks.id,  
            english=marks.english,  
            tamil=marks.tamil,
            maths=marks.maths,
            science=marks.science,
            social=marks.social,
            student_id=marks.student_id
        )
        
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code= 404 , detail='Database not found{e}')
    
    finally:
        db.close()

# Read the Marks by id
@mark_router.get("/mark/{mark_id}", response_model=MarkResponse)
def read_marks_details_by_id(mark_id: int, db: Session = Depends(get_db)):
    try:
        marks = db.query(Mark).filter(Mark.id == mark_id).first()
        if not marks:
            raise HTTPException(status_code=404, detail='Mark detail not found')
        return MarkResponse(
            id=marks.id,  
            english=marks.english,  
            tamil=marks.tamil,
            maths=marks.maths,
            science=marks.science,
            social=marks.social,
            student_id=marks.student_id
        )
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException ( status_code= 404, detail='Mark not found{e}')
    
    finally:
        db.close()