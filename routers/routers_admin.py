from fastapi import APIRouter, HTTPException , status
from schemas.schemas import ClassTable , Teacher , Timetable , CalendarEvent
from database import db_create_class_table, db_fetch_students_from_class_admin, db_add_student_to_class, \
    db_delete_student_from_class, db_create_pending_fee_table, db_add_student_fee_record, db_get_fee_status
from database import db_create_teacher_records_table , db_fetch_all_teacher_records , db_insert_teacher_record , db_delete_teacher_record
from database import db_create_timetable_table , db_fetch_all_timetable_records , db_add_timetable_record , db_delete_timetable_record
from database import db_create_calendar_table , db_fetch_all_calendar_events , db_add_calendar_event , db_delete_calendar_event

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

@router.get("/fetchstudents/{class_number}/{section}")
def fetch_students_from_class(class_number: str, section: str):
    students = db_fetch_students_from_class_admin(class_number, section)
    return students

@router.post("/createteacherrecordstable", status_code=status.HTTP_201_CREATED)
def create_teacher_records_table():
    response = db_create_teacher_records_table()
    if "error" in response:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=response["error"])
    return {"Table": "Teacher_records table created successfully."}

@router.post("/addteacherrecord", status_code=status.HTTP_201_CREATED)
def add_teacher_record(teacher: Teacher):
    response = db_insert_teacher_record(teacher)
    if "error" in response:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=response["error"])
    return {"message": "Teacher record added successfully."}

@router.get("/fetchteacherrecords",)
def fetch_teacher_records():
    teachers = db_fetch_all_teacher_records()
    return teachers

@router.delete("/deleteteacherrecord/{teacher_id}", status_code=status.HTTP_200_OK)
def delete_teacher_record(teacher_id: int):
    response = db_delete_teacher_record(teacher_id)
    if "error" in response:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=response["error"])
    return {"message": "Teacher record deleted successfully."}


@router.post("/createtimetabletable", status_code=status.HTTP_201_CREATED)
def create_timetable_table():
    response = db_create_timetable_table()
    if "error" in response:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=response["error"])
    return {"Table": "Time_table table created successfully."}

@router.post("/addtimetablerecord", status_code=status.HTTP_201_CREATED)
def add_timetable_record(timetable: Timetable):
    response = db_add_timetable_record(timetable)
    if "error" in response:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=response["error"])
    return {"message": "Timetable record added successfully."}

@router.get("/fetchtimetablerecords")
def fetch_timetable_records():
    timetables = db_fetch_all_timetable_records()
    return timetables

@router.delete("/deletetimetablerecord/{sr_no}", status_code=status.HTTP_200_OK)
def delete_timetable_record(sr_no: int):
    response = db_delete_timetable_record(sr_no)
    if "error" in response:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=response["error"])
    return {"message": "Timetable record deleted successfully."}

@router.post("/createcalendartable", status_code=status.HTTP_201_CREATED)
def create_calendar_table():
    response = db_create_calendar_table()
    if "error" in response:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=response["error"])
    return {"Table": "Calendar table created successfully."}

@router.post("/addcalendarevent", status_code=status.HTTP_201_CREATED)
def add_calendar_event(event: CalendarEvent):
    response = db_add_calendar_event(event)
    if "error" in response:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=response["error"])
    return {"message": "Calendar event added successfully."}

@router.get("/fetchcalendarevents")
def fetch_calendar_events():
    events = db_fetch_all_calendar_events()
    return events

@router.delete("/deletecalendarevent/{sr_no}", status_code=status.HTTP_200_OK)
def delete_calendar_event(sr_no: int):

    response = db_delete_calendar_event(sr_no)
    if "error" in response:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=response["error"])
    return {"message": "Calendar event deleted successfully."}

#fee records
@router.post("/creatependingfeetable", status_code=status.HTTP_201_CREATED)
def create_pending_fee_table():
    response = db_create_pending_fee_table()
    if "error" in response:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=response["error"])
    return {"message": "Pending_Fee table created successfully."}


@router.post("/addstudentfeerecord/{adm_no}/{standard}/{fees}", status_code=status.HTTP_201_CREATED)
def add_student_fee_record(adm_no: str, standard: str, fees: str):
    response = db_add_student_fee_record(adm_no, standard, fees)
    if "error" in response:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=response["error"])
    return {"message": "Student fee record added successfully."}

@router.get("/getstatusof/{adm_no}/{month}")
def get_fee_status(adm_no: str, month: str):
    response = db_get_fee_status(adm_no, month)
    if "error" in response:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=response["error"])
    elif "message" in response:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=response["message"])
    return response