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

        # Add the new column if it doesn't exist
        add_column_query = f"ALTER TABLE {table_name} ADD COLUMN IF NOT EXISTS {attendance_column} VARCHAR(10)"
        cursor.execute(add_column_query)
        conn.commit()

        for student_roll_number, status in attendance_data.items():
            query = f"UPDATE {table_name} SET {attendance_column} = %s WHERE roll_number = %s"
            cursor.execute(query, (status, student_roll_number))
        conn.commit()

        return {"message": "Attendance marked successfully"}
    except Exception as e:
        return {"error": str(e)}

# database.py

def db_add_marks(standard: str, section: str, subject: str, marks_data: list):
    try:
        table_name = f"class{standard}{section}"
        current_date = datetime.now().strftime("%d%m")  # Get current date and month in DDMM format
        marks_column = f"marks_{subject}_{current_date}"  # New column name

        # Add the new column if it doesn't exist
        add_column_query = f"ALTER TABLE {table_name} ADD COLUMN IF NOT EXISTS {marks_column} INT"
        cursor.execute(add_column_query)
        conn.commit()

        for entry in marks_data:
            roll_number = entry["roll_number"]
            marks = entry["marks"]
            update_query = f"UPDATE {table_name} SET {marks_column} = %s WHERE roll_number = %s"
            cursor.execute(update_query, (marks, roll_number))
        conn.commit()

        return {"message": "Marks added successfully"}
    except Exception as e:
        return {"error": str(e)}


def db_get_attendance(standard: str, section: str):
    try:
        table_name = f"class{standard}{section}"

        # Query to fetch all columns from the table
        query = f"SELECT * FROM {table_name}"
        cursor.execute(query)
        records = cursor.fetchall()

        return records
    except Exception as e:
        return {"error": str(e)}


def db_get_marks(standard: str, section: str):
    try:
        table_name = f"class{standard}{section}"

        # Query to fetch all columns from the table
        query = f"SELECT * FROM {table_name}"
        cursor.execute(query)
        records = cursor.fetchall()

        return records
    except Exception as e:
        return {"error": str(e)}


# database.py for homework

def db_fetch_homework_by_standard_section(standard: str, section: str):
    try:
        query = """
        SELECT * FROM homework_table
        WHERE standard = %s AND section = %s
        """
        cursor.execute(query, (standard, section))
        homework_data = cursor.fetchall()
        return homework_data
    except Exception as e:
        return {"error": str(e)}


def db_create_homework_table():
    try:
        query = """
        CREATE TABLE IF NOT EXISTS homework_table (
            id SERIAL PRIMARY KEY,
            standard VARCHAR(10) NOT NULL,
            section VARCHAR(10) NOT NULL,
            subject VARCHAR(100) NOT NULL,
            monday TEXT DEFAULT 'yet to be added',
            tuesday TEXT DEFAULT 'yet to be added',
            wednesday TEXT DEFAULT 'yet to be added',
            thursday TEXT DEFAULT 'yet to be added',
            friday TEXT DEFAULT 'yet to be added',
            saturday TEXT DEFAULT 'yet to be added'
        )
        """
        cursor.execute(query)
        conn.commit()
        return {"message": "homework_table created successfully"}
    except Exception as e:
        return {"error": str(e)}

def db_add_class_homework(homework_data):
    try:
        query = """
        INSERT INTO homework_table (standard, section, subject, monday, tuesday, wednesday, thursday, friday, saturday)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (
            homework_data.standard, homework_data.section, homework_data.subject,
            homework_data.monday, homework_data.tuesday, homework_data.wednesday,
            homework_data.thursday, homework_data.friday, homework_data.saturday
        ))
        conn.commit()
        return {"message": f"Default homework added for {homework_data.standard}-{homework_data.section} {homework_data.subject}"}
    except Exception as e:
        return {"error": str(e)}

def db_update_homework(standard: str, section: str, subject: str, day: str, text: str):
    try:
        query = """
        SELECT id FROM homework_table
        WHERE standard = %s AND section = %s AND subject = %s
        """
        cursor.execute(query, (standard, section, subject))
        row = cursor.fetchone()

        if not row:
            return {"error": "Homework data not found"}

        update_query = f"""
        UPDATE homework_table
        SET {day} = %s
        WHERE id = %s
        """
        cursor.execute(update_query, (text, row["id"]))
        conn.commit()

        return {"message": f"{day}'s homework updated successfully"}
    except Exception as e:
        return {"error": str(e)}


# database.py

def db_fetch_homework_by_standard_section_subject(standard: str, section: str, subject: str):
    try:
        query = """
        SELECT * FROM homework_table
        WHERE standard = %s AND section = %s AND subject = %s
        """
        cursor.execute(query, (standard, section, subject))
        homework_data = cursor.fetchall()
        return homework_data
    except Exception as e:
        return {"error": str(e)}


#Student Methods


def db_validate_student(standard: str, section: str, roll_number: int, password: str):
    try:
        table_name = f"class{standard}{section}"
        query = f"SELECT * FROM {table_name} WHERE roll_number = %s"
        cursor.execute(query, (roll_number,))
        student_info = cursor.fetchone()

        if student_info:
            # Assuming the password is stored in the 'password' field of the database
            db_password = student_info.get('password')

            if db_password == password:
                return student_info
            else:
                return None  # Passwords don't match, return None
        else:
            return None  # Student not found in the database

    except Exception as e:
        return None


def db_get_student_info(standard: str, section: str, roll_number: int):
    try:
        table_name = f"class{standard}{section}"
        query = f"SELECT * FROM {table_name} WHERE roll_number = %s"
        cursor.execute(query, (roll_number,))
        student_info = cursor.fetchone()
        print(student_info)
        return student_info
    except Exception as e:
        return None

def db_validate_parent(standard: str, section: str, roll_number: int, password: str):
    try:
        table_name = f"class{standard}{section}"
        query = f"SELECT * FROM {table_name} WHERE roll_number = %s"
        cursor.execute(query, (roll_number,))
        student_info = cursor.fetchone()

        if student_info:
            # Assuming the password is stored in the 'password' field of the database
            db_password = student_info.get('parent_password')

            if db_password == password:
                return student_info
            else:
                return None  # Passwords don't match, return None
        else:
            return None  # Student not found in the database

    except Exception as e:
        return None


def db_fetch_timetable_records_by_standard_section(standard: str, section: str):
    try:
        query = "SELECT * FROM Time_table WHERE Standard = %s AND Section = %s"
        values = (standard, section)
        cursor.execute(query, values)
        timetables = cursor.fetchall()
        return timetables
    except Exception as e:
        return {"error": str(e)}



#Payment database codes(methods)


def db_create_payment_tables():
    query = """
    CREATE TABLE IF NOT EXISTS Order_table (
        order_ID VARCHAR(255),
        adm_no VARCHAR(255),
        fee_amount VARCHAR(255),
        date_created VARCHAR(4),
        date_modified VARCHAR(4)
    );
    CREATE TABLE IF NOT EXISTS Transaction_table (
        transaction_ID VARCHAR(255),
        order_ID VARCHAR(255),
        payment_signature VARCHAR(255) DEFAULT 'yet to be added',
        payment_status VARCHAR(255) DEFAULT 'pending'
    );
    """
    values = ()
    cursor.execute(query, values)
    conn.commit()

def db_create_order(order_id: str, adm_no: str, fee_amount: str, date_created: str, date_modified: str):
    query = """
    INSERT INTO Order_table (order_ID, adm_no, fee_amount, date_created, date_modified)
    VALUES (%s, %s, %s, %s, %s);
    """
    values = (order_id, adm_no, fee_amount, date_created, date_modified)
    cursor.execute(query, values)
    conn.commit()

def db_create_transaction(order_id: str, transaction_id: str):
    query = """
    INSERT INTO Transaction_table (order_ID, transaction_ID)
    VALUES (%s, %s);
    """
    values = (order_id, transaction_id)
    cursor.execute(query, values)
    conn.commit()

def db_update_transaction(order_id: str, payment_signature: str, staitus: str):
    query = """
    UPDATE Transaction_table
    SET payment_signature = %s, payment_status = %s
    WHERE order_ID = %s;
    """
    values = (payment_signature, staitus, order_id)
    cursor.execute(query, values)
    conn.commit()


#fee_table

def db_create_pending_fee_table():
    try:
        query = """
        CREATE TABLE IF NOT EXISTS Pending_Fee (
            adm_no VARCHAR(255),
            standard VARCHAR(255),
            fees VARCHAR(255),
            september VARCHAR(255) DEFAULT 'pending',
            october VARCHAR(255) DEFAULT 'pending',
            november VARCHAR(255) DEFAULT 'pending',
            december VARCHAR(255) DEFAULT 'pending',
            january VARCHAR(255) DEFAULT 'pending',
            february VARCHAR(255) DEFAULT 'pending',
            march VARCHAR(255) DEFAULT 'pending'
        )
        """
        cursor.execute(query)
        conn.commit()
        return {"message": "Pending_Fee table created successfully"}
    except Exception as e:
        return {"error": str(e)}

def db_add_student_fee_record(adm_no: str, standard: str, fees: str):
    try:
        query = """
        INSERT INTO Pending_Fee (adm_no, standard, fees)
        VALUES (%s, %s, %s)
        """
        values = (adm_no, standard, fees)
        cursor.execute(query, values)
        conn.commit()
        return {"message": "Student fee record added successfully"}
    except Exception as e:
        return {"error": str(e)}

def db_get_student_fee(adm_no: str, month: str):
    try:
        # Ensure the provided month matches the column name (e.g., "september", "october", etc.)
        if month.lower() not in ["september", "october", "november", "december", "january", "february", "march"]:
            raise ValueError("Invalid month provided")

        query = f"SELECT {month} FROM Pending_Fee WHERE adm_no = %s"
        cursor.execute(query, (adm_no,))
        fee_status = cursor.fetchone()

        if fee_status:
            return {"fee_status": fee_status[month]}
        else:
            return {"message": f"No fee record found for adm_no {adm_no}"}
    except Exception as e:
        return {"error": str(e)}

def db_update_fee_status(adm_no: str, month: str, date: str):
    try:
        # Ensure the provided month matches the column name (e.g., "september", "october", etc.)
        if month.lower() not in ["september", "october", "november", "december", "january", "february", "march"]:
            raise ValueError("Invalid month provided")

        # Construct the new fee status value in the format "submitter_date"
        new_status = f"submitted_{date}"

        query = f"UPDATE Pending_Fee SET {month} = %s WHERE adm_no = %s"
        cursor.execute(query, (new_status, adm_no,))
        conn.commit()

        return {"message": f"Fee status for {month} updated to {new_status}"}
    except Exception as e:
        return {"error": str(e)}

def db_get_fee_status(adm_no: str, month: str):
    try:
        # Ensure the provided month matches the column name (e.g., "september", "october", etc.)
        if month.lower() not in ["september", "october", "november", "december", "january", "february", "march"]:
            raise ValueError("Invalid month provided")

        query = f"SELECT {month} FROM Pending_Fee WHERE adm_no = %s"
        cursor.execute(query, (adm_no,))
        fee_status = cursor.fetchone()

        if fee_status:
            return {"status": fee_status[month]}
        else:
            return {"message": f"No fee record found for adm_no {adm_no}"}
    except Exception as e:
        return {"error": str(e)}
