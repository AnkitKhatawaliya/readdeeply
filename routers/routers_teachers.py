from fastapi import APIRouter, HTTPException , status
from database import db_validate_teacher_credentials
from database import db_table_exists , db_fetch_students_from_class
from database import db_mark_student_attendance
from typing import List, Dict, Union
from database import db_add_marks


router = APIRouter()



@router.get("/isteacher/{teacher_id}/{password}")
def is_teacher(teacher_id: str, password: str):
    result = db_validate_teacher_credentials(teacher_id, password)

    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Teacher with ID not found")
    if result is False:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect password")
    if result is True:
        raise HTTPException(status_code=status.HTTP_504_GATEWAY_TIMEOUT, detail=" Something went Wrong")
    else:
        return result


@router.get("/getclassrecords/{standard}/{section}")
def get_class_records(standard: str, section: str):
    table_name = f"class{standard}{section}"

    if not db_table_exists(table_name):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Class records not found")

    class_records = db_fetch_students_from_class(standard, section)
    formatted_records = [{"roll_number": record["roll_number"], "name": record["name"]} for record in class_records]

    return formatted_records

@router.post("/mark_attendance/{standard}/{section}")
def mark_attendance(
    standard: str,
    section: str,
    attendance_data: dict
):
    if not db_table_exists(f"class{standard}{section}"):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Class records not found")

    # Mark student attendance
    response = db_mark_student_attendance(standard, section, attendance_data)

    return response


@router.post("/add_marks/{standard}/{section}/{subject}")
def add_marks(standard: str, section: str, subject: str, marks_data: List[Dict[str, Union[str, int]]]):
    if not db_table_exists(f"class{standard}{section}"):
        raise HTTPException(status_code=404, detail="Class records not found")

    response = db_add_marks(standard, section, subject, marks_data)
    if "error" in response:
        raise HTTPException(status_code=500, detail="Error adding marks to the database")

    return response
