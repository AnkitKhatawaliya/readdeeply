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
