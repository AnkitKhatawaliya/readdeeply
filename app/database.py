import psycopg2
from psycopg2.extras import RealDictCursor

# Global variables to store the connection and cursor objects
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

# Global variables to store the connection and cursor objects
dsn = "postgres://ankitkmr1709:PAOscY8uf2qE@ep-flat-bread-71003837.ap-southeast-1.aws.neon.tech/neondb"
conn = psycopg2.connect(dsn, cursor_factory=RealDictCursor)

cursor = conn.cursor()
print("Connection was successful.")


def table_exists(table_name):
    # Check if a table exists in the database
    cursor.execute("SELECT EXISTS(SELECT 1 FROM information_schema.tables WHERE table_name = %s)", (table_name,))
    return cursor.fetchone()["exists"]

def create_students_table(table_name):
    # Create a new table with the required columns
    create_table_query = f"""
        CREATE TABLE {table_name} (
            id SERIAL PRIMARY KEY,
            rollnumber SERIAL,
            name VARCHAR(100) NOT NULL,
            dob VARCHAR(8) NOT NULL,
            gender VARCHAR(10) NOT NULL,
            parent_name VARCHAR(100) NOT NULL,
            parent_mobile VARCHAR(20) NOT NULL
        )
    """
    cursor.execute(create_table_query)
    conn.commit()

def insert_student(table_name, student_data):
    # Insert a new student record into the table
    insert_query = f"""
        INSERT INTO {table_name} (name, dob, gender, parent_name, parent_mobile)
        VALUES (%(name)s, %(dob)s, %(gender)s, %(parent_name)s, %(parent_mobile)s)
    """
    cursor.execute(insert_query, student_data)
    conn.commit()

def get_students(table_name):
    # Retrieve all student records from the table
    select_query = f"""
        SELECT * FROM {table_name}
    """
    cursor.execute(select_query)
    return cursor.fetchall()

def delete_student(table_name, roll_number):
    # Delete a student record from the table by roll number
    delete_query = f"""
        DELETE FROM {table_name}
        WHERE rollnumber = %(roll_number)s
        RETURNING *
    """
    cursor.execute(delete_query, {'roll_number': roll_number})
    deleted_student = cursor.fetchone()
    conn.commit()
    return deleted_student

def table_exists(table_name):
    # Check if a table exists in the database
    cursor.execute("SELECT EXISTS(SELECT 1 FROM information_schema.tables WHERE table_name = %s)", (table_name,))
    return cursor.fetchone()["exists"]

def create_teachers_table(table_name):
    # Create a new table with the required columns
    create_table_query = f"""
        CREATE TABLE {table_name} (
            name VARCHAR(100),
            id VARCHAR(100) PRIMARY KEY,
            yearOfJoining VARCHAR(20),
            degree VARCHAR(100),
            primaryClass VARCHAR(100),
            subject VARCHAR(100),
            phoneNumber VARCHAR(20)
        )
    """
    cursor.execute(create_table_query)
    conn.commit()

def insert_teacher(table_name, teacher_data):
    # Insert a new teacher record into the table
    insert_query = f"""
        INSERT INTO {table_name} (name, id, yearOfJoining, degree, primaryClass, subject, phoneNumber)
        VALUES (%(name)s, %(id)s, %(yearOfJoining)s, %(degree)s, %(primaryClass)s, %(subject)s, %(phoneNumber)s)
    """
    cursor.execute(insert_query, teacher_data)
    conn.commit()

def get_teachers(table_name):
    # Retrieve all teacher records from the table
    select_query = f"""
        SELECT * FROM {table_name}
    """
    cursor.execute(select_query)
    return cursor.fetchall()

def delete_teacher(table_name, teacher_id):
    # Delete a teacher record from the table by ID
    delete_query = f"""
        DELETE FROM {table_name}
        WHERE id = %(teacher_id)s
        RETURNING *
    """
    cursor.execute(delete_query, {'teacher_id': teacher_id})
    deleted_teacher = cursor.fetchone()
    conn.commit()
    return deleted_teacher

# ... (your existing code)

def create_timetable_table(table_name):
    # Create a new timetable table with the required columns
    create_table_query = f"""
        CREATE TABLE {table_name} (
            id SERIAL PRIMARY KEY,
            standard VARCHAR(10) NOT NULL,
            section VARCHAR(10) NOT NULL,
            weekday VARCHAR(20) NOT NULL,
            lect1 VARCHAR(20) NOT NULL,
            lect2 VARCHAR(20) NOT NULL,
            lect3 VARCHAR(20) NOT NULL,
            lect4 VARCHAR(20) NOT NULL,
            lect5 VARCHAR(20) NOT NULL,
            lect6 VARCHAR(20) NOT NULL,
            lect7 VARCHAR(20) NOT NULL,
            lect8 VARCHAR(20) NOT NULL
        )
    """
    cursor.execute(create_table_query)
    conn.commit()

def insert_timetable(table_name, timetable_data):
    # Insert a new timetable record into the table
    insert_query = f"""
        INSERT INTO {table_name} (standard, section, weekday, lect1, lect2, lect3, lect4, lect5, lect6, lect7, lect8)
        VALUES (%(standard)s, %(section)s, %(weekday)s, %(lect1)s, %(lect2)s, %(lect3)s, %(lect4)s, %(lect5)s, %(lect6)s, %(lect7)s, %(lect8)s)
    """
    cursor.execute(insert_query, timetable_data)
    conn.commit()

def get_timetable(table_name):
    # Retrieve all timetable records from the table
    select_query = f"""
        SELECT * FROM {table_name}
    """
    cursor.execute(select_query)
    return cursor.fetchall()

def delete_timetable(table_name, timetable_id):
    # Delete a timetable record from the table by ID
    delete_query = f"""
        DELETE FROM {table_name}
        WHERE id = %(timetable_id)s
        RETURNING *
    """
    cursor.execute(delete_query, {'timetable_id': timetable_id})
    deleted_timetable = cursor.fetchone()
    conn.commit()
    return deleted_timetable

def create_eventannouncement_table(table_name):
    # Create a new table for event and announcement with the required columns
    create_table_query = f"""
        CREATE TABLE {table_name} (
            id SERIAL PRIMARY KEY,
            date VARCHAR(20),
            type VARCHAR(100),
            title VARCHAR(200),
            description TEXT
        )
    """
    cursor.execute(create_table_query)
    conn.commit()

def insert_eventannouncement(table_name, eventannouncement_data):
    # Insert a new event and announcement record into the table
    insert_query = f"""
        INSERT INTO {table_name} (date, type, title, description)
        VALUES (%(date)s, %(type)s, %(title)s, %(description)s)
    """
    cursor.execute(insert_query, eventannouncement_data)
    conn.commit()

def get_eventannouncements(table_name):
    # Retrieve all event and announcement records from the table
    select_query = f"""
        SELECT * FROM {table_name}
    """
    cursor.execute(select_query)
    return cursor.fetchall()

def delete_eventannouncement(table_name, eventannouncement_id):
    # Delete an event and announcement record from the table by ID
    delete_query = f"""
        DELETE FROM {table_name}
        WHERE id = %(eventannouncement_id)s
        RETURNING *
    """
    cursor.execute(delete_query, {'eventannouncement_id': eventannouncement_id})
    deleted_eventannouncement = cursor.fetchone()
    conn.commit()
    return deleted_eventannouncement

