from fastapi import APIRouter, HTTPException, status
from database import db_create_pending_fee_table, db_add_student_fee_record, db_get_fee_status
from database import db_create_payment_tables, db_create_order, db_create_transaction, db_update_transaction
from database import db_get_student_fee, db_update_fee_status

router = APIRouter()


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