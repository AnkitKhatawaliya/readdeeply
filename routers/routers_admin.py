from fastapi import APIRouter, HTTPException , status
from schemas.schemas import ClassTable
from database import db_create_class_table, db_fetch_students_from_class, db_add_student_to_class, db_delete_student_from_class
from typing import List

router = APIRouter()


@router.post("/createclasstable", status_code=status.HTTP_201_CREATED)
def create_class_table(class_number: str, section: str):
    response = db_create_class_table(class_number, section)
    if "error" in response:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=response["error"])
    return {"Table ":"Created successfully."}



@router.post("/addstudent/{class_number}/{section}", status_code=status.HTTP_201_CREATED)
def add_student_to_class(class_number: str, section: str, student: ClassTable):
    response = db_add_student_to_class(class_number, section, student)
    if response:
        return {"message": "Student added successfully"}
    else:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Student addition failed")

@router.delete("/deletestudent/{class_number}/{section}/{roll_number}", status_code=status.HTTP_200_OK)
def delete_student_from_class(class_number: str, section: str, roll_number: int):
    response = db_delete_student_from_class(class_number, section, roll_number)
    if response:
        return {"message": "Student deleted successfully"}
    else:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Student deletion failed")

@router.get("/fetchstudents/{class_number}/{section}", response_model=List[ClassTable])
def fetch_students_from_class(class_number: str, section: str):
    students = db_fetch_students_from_class(class_number, section)
    return students
