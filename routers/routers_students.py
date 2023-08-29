from fastapi import APIRouter, HTTPException, status
from database import db_validate_student, db_get_student_info

router = APIRouter()

@router.get("/validate_student/{standard}/{section}/{roll_number}/{password}", status_code=status.HTTP_200_OK)
def validate_student_login(standard: str, section: str, roll_number: int, password: str):
    is_valid = db_validate_student(standard, section, roll_number, password)
    if is_valid:
        # Set session data and respond with success
        # You should implement the logic to store session data here
        return {"message": "Student login successful"}
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid student credentials")

@router.get("/needstudentinfo/{standard}/{section}/{roll_number}", response_model=dict)
def get_student_info(standard: str, section: str, roll_number: int):
    student_info = db_get_student_info(standard, section, roll_number)
    if student_info:
        return student_info
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student data not found")
