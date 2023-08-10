from fastapi import APIRouter, HTTPException
from database import table_exists
from database import create_students_table , insert_student ,delete_student , get_students
from database import create_teachers_table , insert_teacher ,delete_teacher , get_teachers
from database import create_eventannouncement_table , delete_eventannouncement , get_eventannouncements , insert_eventannouncement
from fastapi import APIRouter, HTTPException
from database import create_timetable_table, insert_timetable, get_timetable, delete_timetable
from schemas.schemas import StudentCreate , TeacherCreate , TimetableCreate , EventAnnouncementCreate
from typing import List

router = APIRouter()

# Students Endpoints

@router.post("/students/add", response_model=StudentCreate)
def add_student(student_data: StudentCreate):
    table_name = "students"
    if not table_exists(table_name):
        create_students_table(table_name)

    # Convert Pydantic model to dictionary
    student_data_dict = student_data.dict()

    # Insert the student record into the table
    insert_student(table_name, student_data_dict)

    return student_data

@router.get("/students/getall", response_model=List[StudentCreate])
def get_all_students():
    table_name = "students"
    if not table_exists(table_name):
        create_students_table(table_name)

    students = get_students(table_name)  # Implement get_students function
    return students

@router.delete("/students/delete/{roll_number}", response_model=StudentCreate)
def delete_student_by_roll_number(roll_number: int):
    table_name = "students"
    if not table_exists(table_name):
        raise HTTPException(status_code=404, detail="Table not found")

    deleted_student = delete_student(table_name, roll_number)  # Implement delete_student function
    return deleted_student

# Teachers Endpoints

@router.post("/teachers/add", response_model=TeacherCreate)
def add_teacher(teacher_data: TeacherCreate):
    table_name = "teachers"
    if not table_exists(table_name):
        create_teachers_table(table_name)

    # Convert Pydantic model to dictionary
    teacher_data_dict = teacher_data.dict()

    # Insert the teacher record into the table
    insert_teacher(table_name, teacher_data_dict)

    return teacher_data

@router.get("/teachers/getall", response_model=List[TeacherCreate])
def get_all_teachers():
    table_name = "teachers"
    if not table_exists(table_name):
        create_teachers_table(table_name)

    teachers = get_teachers(table_name)  # Implement get_teachers function
    return teachers

@router.delete("/teachers/delete/{teacher_id}", response_model=TeacherCreate)
def delete_teacher_by_id(teacher_id: str):
    table_name = "teachers"
    if not table_exists(table_name):
        raise HTTPException(status_code=404, detail="Table not found")

    deleted_teacher = delete_teacher(table_name, teacher_id)  # Implement delete_teacher function
    return deleted_teacher

@router.post("/timetable/add", response_model=dict)
def add_timetable(timetable_data: TimetableCreate):
    table_name = "timetable"
    if not table_exists(table_name):
        create_timetable_table(table_name)

    # Insert the timetable record into the table
    insert_timetable(table_name, timetable_data.dict())

    return {"message": "Timetable added successfully"}

@router.get("/timetable/get", response_model=List[TimetableCreate])
def get_timetable_records():
    table_name = "timetable"
    if not table_exists(table_name):
        create_timetable_table(table_name)

    timetable_records = get_timetable(table_name)
    return timetable_records

@router.delete("/timetable/delete/{timetable_id}", response_model=dict)
def delete_timetable_record(timetable_id: int):
    table_name = "timetable"
    if not table_exists(table_name):
        raise HTTPException(status_code=404, detail="Timetable table not found")

    # Delete the timetable record from the table
    deleted_timetable = delete_timetable(table_name, timetable_id)

    return {"message": "Timetable record deleted successfully", "deleted_timetable": deleted_timetable}


@router.post("/eventannouncement/add", response_model=dict)
def add_eventannouncement(eventannouncement_data: EventAnnouncementCreate):
    table_name = "eventannouncement"

    # Insert the eventannouncement record into the table
    insert_eventannouncement(table_name, eventannouncement_data.dict())

    return {"message": "Event or Announcement added successfully"}

@router.get("/eventannouncement/get", response_model=List[EventAnnouncementCreate])
def get_eventannouncement_records():
    table_name = "eventannouncement"
    if not table_exists(table_name):
        create_eventannouncement_table(table_name)

    eventannouncement_records = get_eventannouncements(table_name)
    return eventannouncement_records

@router.delete("/eventannouncement/delete/{eventannouncement_id}", response_model=dict)
def delete_eventannouncement_record(eventannouncement_id: int):
    table_name = "eventannouncement"

    # Delete the eventannouncement record from the table
    deleted_eventannouncement = delete_eventannouncement(table_name, eventannouncement_id)

    return {"message": "Event or Announcement record deleted successfully", "deleted_eventannouncement": deleted_eventannouncement}

