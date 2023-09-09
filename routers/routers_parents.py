from fastapi import APIRouter, HTTPException, status

from database import db_validate_parent, db_get_student_info, db_fetch_homework_by_standard_section, \
    db_fetch_all_calendar_events, db_fetch_timetable_records_by_standard_section, db_get_attendance, db_get_marks, \
    db_create_order, db_create_transaction, db_create_payment_tables, db_update_transaction, db_get_student_fee, \
    db_update_fee_status

router = APIRouter()

@router.get("/validate_parent/{standard}/{section}/{roll_number}/{password}", status_code=status.HTTP_200_OK)
def validate_parent_login(standard: str, section: str, roll_number: str, password: str):
    roll_number_int = int(roll_number)  # Convert the string to an integer
    is_valid = db_validate_parent(standard, section, roll_number_int, password)
    if is_valid:
        # Set session data and respond with success
        # You should implement the logic to store session data here
        return {"message": "Parent login successful"}
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


@router.get("/fetch_homework/{standard}/{section}",)
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



#payment endpoints

@router.post("/createpaymenttable", status_code=status.HTTP_201_CREATED)
def create_payment_table():
    try:
        db_create_payment_tables()
        return {"message": "Payment tables created successfully"}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.post("/transactionstarted/{order_ID}/{adm_no}/{fee_amount}/{date_created}/{date_modified}/{transaction_ID}", status_code=status.HTTP_201_CREATED)
def transaction_started(
    order_ID: str,
    adm_no: str,
    fee_amount: str,
    date_created: str,
    date_modified: str,
    transaction_ID: str
):
    try:
        # Create Order entry with order_ID, date_created, and date_modified
        db_create_order(order_ID, adm_no, fee_amount, date_created, date_modified)

        # Create Transaction entry with order_ID and transaction_ID
        db_create_transaction(order_ID, transaction_ID)

        return {"message": "Transaction started successfully"}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=str(e))

@router.post("/transactionSuccessful/{order_id}/{payment_signature}/{staitus}", status_code=status.HTTP_200_OK)
def transaction_successful(order_id: str, payment_signature: str, staitus: str):
    try:
        # Update Transaction entry with order_id
        db_update_transaction(order_id, payment_signature, staitus)

        return {"message": "Transaction updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=str(e))

#get the fee


@router.get("/getstudentfee/{adm_no}/{month}")
def get_student_fee(adm_no: str, month: str):
    response = db_get_student_fee(adm_no, month)
    if "error" in response:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=response["error"])
    elif "message" in response:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=response["message"])
    return response


@router.post("/updatefeestatus/{adm_no}/{month}/{date}", status_code=status.HTTP_200_OK)
def update_fee_status(adm_no: str, month: str, date: str):
    response = db_update_fee_status(adm_no, month, date)
    if "error" in response:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=response["error"])
    return response