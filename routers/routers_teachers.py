from fastapi import APIRouter, HTTPException , status
from typing import List, Dict, Union
from schemas.schemas import Homework, CalendarEvent, Timetable
from database import db_validate_teacher_credentials, db_fetch_students_from_class, db_fetch_all_calendar_events, \
    db_fetch_timetable_records_by_standard_section
from database import db_table_exists , db_fetch_homework_by_standard_section_subject
from database import db_add_marks, db_get_marks, db_mark_student_attendance, db_get_attendance
from database import db_create_homework_table, db_add_class_homework, db_update_homework , db_fetch_homework_by_standard_section


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


@router.get("/create_hw_table", response_model=dict)
def create_homework_table():
    response = db_create_homework_table()
    return response

@router.post("/add_class_hw/{standard}/{section}/{subject}", response_model=dict)
def add_class_homework(standard: str, section: str, subject: str):
    homework_data = Homework(standard=standard, section=section, subject=subject, monday="yet to be added", tuesday="yet to be added", wednesday="yet to be added", thursday="yet to be added", friday="yet to be added", saturday="yet to be added")
    response = db_add_class_homework(homework_data)
    return response

@router.put("/update_homework", response_model=dict)
def update_homework(
    standard: str,
    section: str,
    subject: str,
    day: str,
    text: str
):
    response = db_update_homework(standard, section, subject, day, text)
    if "error" in response:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=response["error"])
    return response



@router.get("/fetch_homework/{standard}/{section}/{subject}", response_model=list)
def fetch_homework_by_standard_section_subject(standard: str, section: str, subject: str):
    homework_data = db_fetch_homework_by_standard_section_subject(standard, section, subject)
    if "error" in homework_data:
        raise HTTPException(status_code=500, detail=homework_data["error"])
    return homework_data

@router.get("/fetchcalendarevents", response_model=List[CalendarEvent])
def fetch_calendar_events():
    events = db_fetch_all_calendar_events()
    return events


@router.get("/fetchtimetablerecords/{standard}/{section}", response_model=List[Timetable])
def fetch_timetable_records_by_standard_section(standard: str, section: str):
    timetables = db_fetch_timetable_records_by_standard_section(standard, section)
    if not timetables:
        raise HTTPException(status_code=404, detail="No matching records found")
    return timetables
