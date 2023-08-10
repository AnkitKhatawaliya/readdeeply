from pydantic import BaseModel

class StudentCreate(BaseModel):
    rollnumber: int
    name: str
    dob: str
    gender: str
    parent_name: str
    parent_mobile: str
    student_password: str  # New field
    parent_password: str   # New field

    class Config:
        orm_mode = True

class TeacherCreate(BaseModel):
    name: str
    id: str
    yearOfJoining: str
    degree: str
    primaryClass: str
    subject: str
    phoneNumber: str
    password: str  # New field

    class Config:
        orm_mode = True

class TimetableCreate(BaseModel):
    standard: str
    section: str
    weekday: str
    lect1: str
    lect2: str
    lect3: str
    lect4: str
    lect5: str
    lect6: str
    lect7: str
    lect8: str

    class Config:
        orm_mode = True

class EventAnnouncementCreate(BaseModel):
    date: str
    mode: str
    title: str
    description: str

    class Config:
        orm_mode = True
