import psycopg2
from psycopg2.extras import RealDictCursor
from schemas.schemas import ClassTable , Teacher , Timetable , CalendarEvent
from datetime import datetime

# conn = psycopg2.connect(
#     host='localhost',
#     database='wow',
#     user='postgres',
#     password='Post@2606',
#     cursor_factory=RealDictCursor
# )
#
# cursor = conn.cursor()
# print("Connection was successful.")


dsn = "postgres://ankitkmr1709:y4Zdg7GMxRVH@ep-hidden-fire-57816100.us-east-2.aws.neon.tech/neondb"
conn = psycopg2.connect(dsn, cursor_factory=RealDictCursor)
cursor = conn.cursor()
print("Connection was successful.")


def db_create_class_table(class_number: str, section: str):
    try:
        table_name = f"class{class_number}{section}"
        query = f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            roll_number SERIAL,
            adm_no VARCHAR(255),
            name VARCHAR(255),
            password VARCHAR(255),
            dob VARCHAR(10),
            gender VARCHAR(10),
            parent_name VARCHAR(255),
            par_con VARCHAR(255),
            parent_password VARCHAR(255)
        )
        """
        cursor.execute(query)
        conn.commit()
        return {"message": f"Table {table_name} created successfully"}  # Return success message
    except Exception as e:
        return {"error": str(e)}  # Return error message


def db_add_student_to_class(class_number: str, section: str, student: ClassTable):
    try:
        table_name = f"class{class_number}{section}"
        query = f"""
        INSERT INTO {table_name} (adm_no, name, password, dob, gender, parent_name, par_con, parent_password)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (
            student.adm_no,
            student.name,
            student.password,
            student.dob,
            student.gender,
            student.parent_name,
            student.par_con,
            student.parent_password
        )
        cursor.execute(query, values)
        conn.commit()
        return {"message": "Student added successfully"}  # Return success message
    except Exception as e:
        return {"error": str(e)}  # Return error message

def db_delete_student_from_class(class_number: str, section: str, roll_number: int):
    try:
        table_name = f"class{class_number}{section}"
        query = f"""
        DELETE FROM {table_name}
        WHERE roll_number = %s
        """
        cursor.execute(query, (roll_number,))
        conn.commit()
        return {"message": "Student deleted successfully"}  # Return success message
    except Exception as e:
        return {"error": str(e)}  # Return error message

def db_fetch_students_from_class_admin(class_number: str, section: str):
    try:
        table_name = f"class{class_number}{section}"
        query = f"SELECT * FROM {table_name}"
        cursor.execute(query)
        students = cursor.fetchall()
        return students  # Return list of students
    except Exception as e:
        return {"error": str(e)}  # Return error message


def db_fetch_students_from_class(class_number: str, section: str):
    try:
        table_name = f"class{class_number}{section}"
        # List the specific columns you want to fetch
        columns_to_fetch = [
            "roll_number",
            "adm_no",
            "name",
            "password",
            "dob",
            "gender",
            "parent_name",
            "par_con",
            "parent_password"
        ]
        columns_str = ", ".join(columns_to_fetch)

        query = f"SELECT {columns_str} FROM {table_name}"
        cursor.execute(query)
        students = cursor.fetchall()
        return students  # Return list of students with specified columns
    except Exception as e:
        return {"error": str(e)}  # Return error message



def db_table_exists(table_name: str):
    try:
        query = f"SELECT 1 FROM {table_name} LIMIT 1"
        cursor.execute(query)
        return True
    except:
        return False

    
def db_create_teacher_records_table():
    try:
        query = """
        CREATE TABLE IF NOT EXISTS Teacher_records (
            ID SERIAL PRIMARY KEY,
            Name VARCHAR(255),
            Primary_class VARCHAR(255),
            Subject VARCHAR(255),
            Date_of_joining VARCHAR(10),
            Degree VARCHAR(255),
            Contact_number VARCHAR(20),
            Other_classes VARCHAR(40),  -- New column added
            Passw VARCHAR(10)  -- New column added
        )
        """
        cursor.execute(query)
        conn.commit()
        return {"message": "Teacher_records table created successfully"}
    except Exception as e:
        return {"error": str(e)}

def db_insert_teacher_record(teacher: Teacher):
    try:
        query = """
        INSERT INTO Teacher_records (Name, Primary_class, Subject, Date_of_joining, Degree, Contact_number, Other_classes, Passw)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)  -- New columns added
        """
        values = (
            teacher.name,
            teacher.primary_class,
            teacher.subject,
            teacher.date_of_joining,
            teacher.degree,
            teacher.contact_number,
            teacher.other_classes,
            teacher.passw  # New column value
        )
        cursor.execute(query, values)
        conn.commit()
        return {"message": "Teacher record added successfully"}
    except Exception as e:
        return {"error": str(e)}

# Your existing db_fetch_all_teacher_records and db_delete_teacher_record methods remain unchanged


def db_fetch_all_teacher_records():
    try:
        query = "SELECT * FROM Teacher_records"
        cursor.execute(query)
        teachers = cursor.fetchall()
        return teachers
    except Exception as e:
        return {"error": str(e)}

def db_delete_teacher_record(teacher_id: int):
    try:
        query = "DELETE FROM Teacher_records WHERE ID = %s"
        cursor.execute(query, (teacher_id,))
        conn.commit()
        return {"message": "Teacher record deleted successfully"}
    except Exception as e:
        return {"error": str(e)}


def db_create_timetable_table():
    try:
        query = """
        CREATE TABLE IF NOT EXISTS Time_table (
            Sr_no SERIAL PRIMARY KEY,
            Standard VARCHAR(255),
            Section VARCHAR(255),
            Weekday VARCHAR(255),
            Lect_1 VARCHAR(255),
            Lect_2 VARCHAR(255),
            Lect_3 VARCHAR(255),
            Lect_4 VARCHAR(255),
            Lect_5 VARCHAR(255),
            Lect_6 VARCHAR(255),
            Lect_7 VARCHAR(255),
            Lect_8 VARCHAR(255)
        )
        """
        cursor.execute(query)
        conn.commit()
        return {"message": "Time_table table created successfully"}
    except Exception as e:
        return {"error": str(e)}

def db_add_timetable_record(timetable: Timetable):
    try:
        query = """
        INSERT INTO Time_table (Standard, Section, Weekday, Lect_1, Lect_2, Lect_3, Lect_4, Lect_5, Lect_6, Lect_7, Lect_8)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (
            timetable.standard,
            timetable.section,
            timetable.weekday,
            timetable.lect_1,
            timetable.lect_2,
            timetable.lect_3,
            timetable.lect_4,
            timetable.lect_5,
            timetable.lect_6,
            timetable.lect_7,
            timetable.lect_8
        )
        cursor.execute(query, values)
        conn.commit()
        return {"message": "Timetable record added successfully"}
    except Exception as e:
        return {"error": str(e)}

def db_fetch_all_timetable_records():
    try:
        query = "SELECT * FROM Time_table"
        cursor.execute(query)
        timetables = cursor.fetchall()
        return timetables
    except Exception as e:
        return {"error": str(e)}

def db_delete_timetable_record(sr_no: int):
    try:
        query = "DELETE FROM Time_table WHERE Sr_no = %s"
        cursor.execute(query, (sr_no,))
        conn.commit()
        return {"message": "Timetable record deleted successfully"}
    except Exception as e:
        return {"error": str(e)}

def db_create_calendar_table():
    try:
        query = """
        CREATE TABLE IF NOT EXISTS Calendar (
            Sr_no SERIAL PRIMARY KEY,
            Date VARCHAR(10),
            Hook VARCHAR(255),
            Title VARCHAR(255),
            Content TEXT
        )
        """
        cursor.execute(query)
        conn.commit()
        return {"message": "Calendar table created successfully"}
    except Exception as e:
        return {"error": str(e)}

def db_add_calendar_event(event: CalendarEvent):
    try:
        query = """
        INSERT INTO Calendar (Date, Hook, Title, Content)
        VALUES (%s, %s, %s, %s)
        """
        values = (
            event.date,
            event.hook,
            event.title,
            event.content
        )
        cursor.execute(query, values)
        conn.commit()
        return {"message": "Calendar event added successfully"}
    except Exception as e:
        return {"error": str(e)}

def db_fetch_all_calendar_events():
    try:
        query = "SELECT * FROM Calendar"
        cursor.execute(query)
        events = cursor.fetchall()
        return events
    except Exception as e:
        return {"error": str(e)}

def db_delete_calendar_event(sr_no: int):
    try:
        query = "DELETE FROM Calendar WHERE Sr_no = %s"
        cursor.execute(query, (sr_no,))
        conn.commit()
        return {"message": "Calendar event deleted successfully"}
    except Exception as e:
        return {"error": str(e)}

#Teacher methods

def db_validate_teacher_credentials(teacher_id: str, password: str):
    try:
        query = "SELECT * FROM Teacher_records WHERE ID = %s"
        cursor.execute(query, (teacher_id,))
        teacher = cursor.fetchone()

        if teacher is None:
            return None  # Teacher not found
        if teacher["passw"] == password:
            return teacher  # Credentials valid
        else:
            return False  # Incorrect password

    except Exception as e:
        return True

def db_fetch_students_from_class(standard: str, section: str):
    try:
        table_name = f"class{standard}{section}"
        query = f"SELECT roll_number, name FROM {table_name}"
        cursor.execute(query)
        students = cursor.fetchall()
        return students  # Return list of students' roll_number and name
    except Exception as e:
        return {"error": str(e)}  # Return error message


def db_mark_student_attendance(standard: str, section: str, attendance_data: dict):
    try:
        table_name = f"class{standard}{section}"
        current_date = datetime.now().strftime("%d%m")  # Get current date and month in DDMM format
        attendance_column = f"att{current_date}"  # New column name

        for student_roll_number, status in attendance_data.items():
            query = f"UPDATE {table_name} SET {attendance_column} = %s WHERE roll_number = %s"
            cursor.execute(query, (status, student_roll_number))
        conn.commit()
        return {"message": "Attendance marked successfully"}
    except Exception as e:
        return {"error": str(e)}
