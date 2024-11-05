from fastapi import FastAPI
from Operation.detailCRUD import *
from Operation.studentCRUD import *
from Operation.markCRUD import *
from Module.modules import * 
from Database.db import *
app = FastAPI()

app.include_router(student_router,tags=['Student'])
app.include_router(detail_router,tags=['Details'])
app.include_router(mark_router,tags=['Marks'])