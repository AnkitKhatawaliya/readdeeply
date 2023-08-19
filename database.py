import psycopg2
from psycopg2.extras import RealDictCursor
from schemas.schemas import ClassTable

# conn = psycopg2.connect(
#     host='localhost',
#     database='deploy',
#     user='postgres',
#     password='Post@2606',
#     cursor_factory=RealDictCursor
# )
#
# cursor = conn.cursor()
# print("Connection was successful.")


dsn = "postgres://ankitkmr1709:PAOscY8uf2qE@ep-flat-bread-71003837.ap-southeast-1.aws.neon.tech/neondb"
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

def db_fetch_students_from_class(class_number: str, section: str):
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