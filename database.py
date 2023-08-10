import psycopg2
from psycopg2.extras import RealDictCursor


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
def table_exists(table_name):
    cursor.execute("SELECT EXISTS(SELECT 1 FROM information_schema.tables WHERE table_name = %s)", (table_name,))
    return cursor.fetchone()["exists"]

def create_students_table(table_name):
    create_table_query = f"""
        CREATE TABLE {table_name} (
            id SERIAL PRIMARY KEY,
            rollnumber SERIAL,
            name VARCHAR(100) NOT NULL,
            dob VARCHAR(8) NOT NULL,
            gender VARCHAR(10) NOT NULL,
            parent_name VARCHAR(100) NOT NULL,
            parent_mobile VARCHAR(20) NOT NULL,
            student_password VARCHAR(100) NOT NULL,  -- New column
            parent_password VARCHAR(100) NOT NULL    -- New column
        )
    """
    cursor.execute(create_table_query)
    conn.commit()

def insert_student_in_class(table_name, student_data):
    insert_query = f"""
        INSERT INTO {table_name} (name, dob, gender, parent_name, parent_mobile, student_password, parent_password)
        VALUES (%(name)s, %(dob)s, %(gender)s, %(parent_name)s, %(parent_mobile)s, %(student_password)s, %(parent_password)s)
    """
    cursor.execute(insert_query, student_data)
    conn.commit()

def get_students_in_class(table_name):
    select_query = f"""
        SELECT * FROM {table_name}
    """
    cursor.execute(select_query)
    return cursor.fetchall()

def delete_student_in_class(table_name, roll_number):
    delete_query = f"""
        DELETE FROM {table_name}
        WHERE rollnumber = %(roll_number)s
        RETURNING *
    """
    cursor.execute(delete_query, {'roll_number': roll_number})
    deleted_student = cursor.fetchone()
    conn.commit()
    return deleted_student


def create_teachers_table(table_name):
    create_table_query = f"""
        CREATE TABLE {table_name} (
            name VARCHAR(100),
            id VARCHAR(100) PRIMARY KEY,
            yearOfJoining VARCHAR(20),
            degree VARCHAR(100),
            primaryClass VARCHAR(100),
            subject VARCHAR(100),
            phoneNumber VARCHAR(20),
            password VARCHAR(100) NOT NULL  -- New column
        )
    """
    cursor.execute(create_table_query)
    conn.commit()

def insert_teacher_in_school(table_name, teacher_data):
    insert_query = f"""
        INSERT INTO {table_name} (name, id, yearOfJoining, degree, primaryClass, subject, phoneNumber, password)
        VALUES (%(name)s, %(id)s, %(yearOfJoining)s, %(degree)s, %(primaryClass)s, %(subject)s, %(phoneNumber)s, %(password)s)
    """
    cursor.execute(insert_query, teacher_data)
    conn.commit()

def get_teachers_in_school(table_name):
    select_query = f"""
        SELECT * FROM {table_name}
    """
    cursor.execute(select_query)
    return cursor.fetchall()

def delete_teacher_in_school(table_name, teacher_id):
    delete_query = f"""
        DELETE FROM {table_name}
        WHERE id = %(teacher_id)s
        RETURNING *
    """
    cursor.execute(delete_query, {'teacher_id': teacher_id})
    deleted_teacher = cursor.fetchone()
    conn.commit()
    return deleted_teacher

# ... (previous code)

def create_timetable_table(table_name):
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

def insert_timetable_record(table_name, timetable_data):
    insert_query = f"""
        INSERT INTO {table_name} (standard, section, weekday, lect1, lect2, lect3, lect4, lect5, lect6, lect7, lect8)
        VALUES (%(standard)s, %(section)s, %(weekday)s, %(lect1)s, %(lect2)s, %(lect3)s, %(lect4)s, %(lect5)s, %(lect6)s, %(lect7)s, %(lect8)s)
    """
    cursor.execute(insert_query, timetable_data)
    conn.commit()

def get_timetable_records(table_name):
    select_query = f"""
        SELECT * FROM {table_name}
    """
    cursor.execute(select_query)
    return cursor.fetchall()

def delete_timetable_record(table_name, timetable_id):
    delete_query = f"""
        DELETE FROM {table_name}
        WHERE id = %(timetable_id)s
        RETURNING *
    """
    cursor.execute(delete_query, {'timetable_id': timetable_id})
    deleted_timetable = cursor.fetchone()
    conn.commit()
    return deleted_timetable

# ... (previous code)

def create_eventannouncement_table(table_name):
    create_table_query = f"""
        CREATE TABLE {table_name} (
            id SERIAL PRIMARY KEY,
            date VARCHAR(20),
            mode VARCHAR(100),  -- Change field name from 'type' to 'mode'
            title VARCHAR(200),
            description TEXT
        )
    """
    cursor.execute(create_table_query)
    conn.commit()

def insert_eventannouncement_record(table_name, eventannouncement_data):
    insert_query = f"""
        INSERT INTO {table_name} (date, mode, title, description)
        VALUES (%(date)s, %(mode)s, %(title)s, %(description)s)
    """
    cursor.execute(insert_query, eventannouncement_data)
    conn.commit()

def get_eventannouncement_records(table_name):
    select_query = f"""
        SELECT * FROM {table_name}
    """
    cursor.execute(select_query)
    return cursor.fetchall()

def delete_eventannouncement_record(table_name, eventannouncement_id):
    delete_query = f"""
        DELETE FROM {table_name}
        WHERE id = %(eventannouncement_id)s
        RETURNING *
    """
    cursor.execute(delete_query, {'eventannouncement_id': eventannouncement_id})
    deleted_eventannouncement = cursor.fetchone()
    conn.commit()
    return deleted_eventannouncement
