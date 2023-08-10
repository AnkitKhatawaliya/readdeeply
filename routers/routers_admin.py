from fastapi import APIRouter, HTTPException
from database import table_exists
from database import create_students_table, insert_student_in_class as db_insert_student, delete_student_in_class as db_delete_student, get_students_in_class as db_get_students
from database import delete_teacher_in_school , get_teachers_in_school , insert_teacher_in_school , create_teachers_table
from database import delete_eventannouncement_record , get_eventannouncement_records , insert_eventannouncement_record , create_eventannouncement_table
from database import delete_timetable_record , get_timetable_records , insert_timetable_record , create_timetable_table
from schemas.schemas import StudentCreate , TeacherCreate , TimetableCreate , EventAnnouncementCreate
from typing import List

router = APIRouter()

@router.post("/students/createtableforclass", response_model=str)
def create_tables_for_class(standard: str, section: str):
    table_name = f"class{standard}{section}"

    if table_exists(table_name):
        return f"Table {table_name} already exists"

    create_students_table(table_name)

    return f"Table {table_name} created successfully"

@router.post("/students/{standard}/{section}/add", response_model=StudentCreate)
def add_a_student_to_class(
    standard: str,
    section: str,
    student_data: StudentCreate
):
    table_name = f"class{standard}{section}"

    if not table_exists(table_name):
        return HTTPException(status_code=404, detail=f"Table {table_name} not found")

    student_data_dict = student_data.dict()

    # Insert the student record into the class-specific table
    db_insert_student(table_name, student_data_dict)

    return student_data

@router.get("/students/{standard}/{section}/getall", response_model=List[StudentCreate])
def get_all_students_in_class(
    standard: str,
    section: str
):
    table_name = f"class{standard}{section}"

    if not table_exists(table_name):
        return HTTPException(status_code=404, detail=f"Table {table_name} not found")

    students = db_get_students(table_name)
    return students

@router.delete("/students/{standard}/{section}/delete/{roll_number}", response_model=StudentCreate)
def delete_a_student_in_class(
    standard: str,
    section: str,
    roll_number: int
):
    table_name = f"class{standard}{section}"

    if not table_exists(table_name):
        return HTTPException(status_code=404, detail=f"Table {table_name} not found")

    deleted_student = db_delete_student(table_name, roll_number)
    return deleted_student

@router.post("/teachers/add", response_model=TeacherCreate)
def add_a_teacher(
    teacher_data: TeacherCreate
):
    table_name = "teachers"

    if not table_exists(table_name):
        create_teachers_table(table_name)

    teacher_data_dict = teacher_data.dict()

    # Insert the teacher record into the teachers table
    insert_teacher_in_school(table_name, teacher_data_dict)

    return teacher_data

@router.get("/teachers/getall", response_model=List[TeacherCreate])
def get_all_teachers():
    table_name = "teachers"

    if not table_exists(table_name):
        create_teachers_table(table_name)

    teachers = get_teachers_in_school(table_name)
    return teachers

@router.delete("/teachers/delete/{teacher_id}", response_model=TeacherCreate)
def delete_a_teacher_by_id(
    teacher_id: str
):
    table_name = "teachers"

    if not table_exists(table_name):
        return HTTPException(status_code=404, detail="Table not found")

    deleted_teacher = delete_teacher_in_school(table_name, teacher_id)
    return deleted_teacher

@router.post("/timetable/add", response_model=dict)
def add_a_time_table_record(timetable_data: TimetableCreate):
    table_name = "timetable"

    if not table_exists(table_name):
        create_timetable_table(table_name)

    insert_timetable_record(table_name, timetable_data.dict())

    return {"message": "Timetable record added successfully"}

@router.get("/timetable/get", response_model=List[TimetableCreate])
def get_all_time_table_records():
    table_name = "timetable"

    if not table_exists(table_name):
        create_timetable_table(table_name)

    timetable_records = get_timetable_records(table_name)
    return timetable_records

@router.delete("/timetable/delete/{timetable_id}", response_model=dict)
def delete_a_time_table_record(timetable_id: int):
    table_name = "timetable"

    if not table_exists(table_name):
        return HTTPException(status_code=404, detail="Table not found")

    deleted_timetable = delete_timetable_record(table_name, timetable_id)

    return {"message": "Timetable record deleted successfully", "deleted_timetable": deleted_timetable}

@router.post("/eventannouncement/add", response_model=dict)
def add_a_eventandannouncement_record(eventannouncement_data: EventAnnouncementCreate):
    table_name = "eventannouncement"

    if not table_exists(table_name):
        create_eventannouncement_table(table_name)

    insert_eventannouncement_record(table_name, eventannouncement_data.dict())

    return {"message": "Event or Announcement record added successfully"}

@router.get("/eventannouncement/get", response_model=List[EventAnnouncementCreate])
def get_all_eventandannouncement_records():
    table_name = "eventannouncement"

    if not table_exists(table_name):
        create_eventannouncement_table(table_name)

    eventannouncement_records = get_eventannouncement_records(table_name)
    return eventannouncement_records

@router.delete("/eventannouncement/delete/{eventannouncement_id}", response_model=dict)
def delete_a_eventandannouncement_record(eventannouncement_id: int):
    table_name = "eventannouncement"

    if not table_exists(table_name):
        return HTTPException(status_code=404, detail="Table not found")

    deleted_eventannouncement = delete_eventannouncement_record(table_name, eventannouncement_id)

    return {"message": "Event or Announcement record deleted successfully", "deleted_eventannouncement": deleted_eventannouncement}
