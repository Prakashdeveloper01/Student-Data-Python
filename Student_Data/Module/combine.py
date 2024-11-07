from pydantic import BaseModel
from typing import List , Optional
from Module.modules import *

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
    
    
    student_details = student.student_details
    
    student_marks = student.student_marks 

    marks_list = []

    if student_marks:
        #for mark in student_marks:
            #marks_list.append(UseMark(
            marks_list = list(map(lambda mark: UseMark(
                tamil=mark.tamil,
                english=mark.english,
                maths=mark.maths,
                science=mark.science,
                social=mark.social,
                student_id=student.id
            ),student_marks))

    combine_response = Combine(
        name=student.name,
        age=student.age,
        qualification=student_details.qualification if student_details else None,
        address=student_details.address if student_details else None,
        student_id=student.id,
        marks=marks_list  
    )

    return combine_response