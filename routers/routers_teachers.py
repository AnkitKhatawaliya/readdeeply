from fastapi import APIRouter, HTTPException , status
from database import db_validate_teacher_credentials
from database import db_table_exists , db_fetch_students_from_class
from typing import List

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
