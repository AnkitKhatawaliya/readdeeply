from fastapi import APIRouter, HTTPException, status
from database import db_validate_student, db_get_student_info, db_fetch_homework_by_standard_section, \
    db_fetch_all_calendar_events, db_fetch_timetable_records_by_standard_section, db_get_attendance, db_get_marks

router = APIRouter()

@router.get("/validate_student/{standard}/{section}/{roll_number}/{password}", status_code=status.HTTP_200_OK)
def validate_student_login(standard: str, section: str, roll_number: str, password: str):
    roll_number_int = int(roll_number)  # Convert the string to an integer
    is_valid = db_validate_student(standard, section, roll_number_int, password)
    if is_valid:
        # Set session data and respond with success
        # You should implement the logic to store session data here
        return {"message": "Student login successful"}
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid student credentials")

@router.get("/needstudentinfo/{standard}/{section}/{roll_number}")
def get_student_info(standard: str, section: str, roll_number: str):
    roll_number_int = int(roll_number)  # Convert the string to an integer
    student_info = db_get_student_info(standard, section, roll_number_int)
    if student_info:
        return student_info
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student data not found")


@router.get("/fetch_homework/{standard}/{section}")
def fetch_homework_by_standard_section(standard: str, section: str):
    homework_data = db_fetch_homework_by_standard_section(standard, section)
    if "error" in homework_data:
        raise HTTPException(status_code=500, detail=homework_data["error"])
    return homework_data

@router.get("/fetchcalendarevents")
def fetch_calendar_events():
    events = db_fetch_all_calendar_events()
    return events

@router.get("/fetchtimetablerecords/{standard}/{section}")
def fetch_timetable_records_by_standard_section(standard: str, section: str):
    timetables = db_fetch_timetable_records_by_standard_section(standard, section)
    if not timetables:
        raise HTTPException(status_code=404, detail="No matching records found")
    return timetables


@router.get("/get_attendance/{standard}/{section}")
def get_attendance(standard: str, section: str):
    attendance_records = db_get_attendance(standard, section)
    if isinstance(attendance_records, dict) and "error" in attendance_records:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=attendance_records["error"])
    return attendance_records


@router.get("/get_marks/{standard}/{section}")
def get_marks(standard: str, section: str):
    marks_records = db_get_marks(standard, section)
    if isinstance(marks_records, dict) and "error" in marks_records:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=marks_records["error"])
    return marks_records

