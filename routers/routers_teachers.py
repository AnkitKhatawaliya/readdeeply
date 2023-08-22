from fastapi import APIRouter, HTTPException , status
from database import db_validate_teacher_credentials
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
