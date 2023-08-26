
from pydantic import BaseModel


class ClassTable(BaseModel):
    roll_number: int
    adm_no: str
    name: str
    password: str
    dob: str
    gender: str
    parent_name: str
    par_con: str
    parent_password: str

    class Config:
        orm_mode = True


class Teacher(BaseModel):
    id: int
    name: str
    primary_class: str
    subject: str
    date_of_joining: str
    degree: str
    contact_number: str
    other_classes: str  # New column added
    passw: str  # New column added

    class Config:
        orm_mode = True


class Timetable(BaseModel):
    sr_no: int
    standard: str
    section: str
    weekday: str
    lect_1: str
    lect_2: str
    lect_3: str
    lect_4: str
    lect_5: str
    lect_6: str
    lect_7: str
    lect_8: str

    class Config:
        orm_mode = True

class CalendarEvent(BaseModel):
    sr_no: int
    date: str
    hook: str
    title: str
    content: str

    class Config:
        orm_mode = True

