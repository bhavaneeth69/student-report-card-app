from db import get_connection

def add_student(name, class_name, roll_number):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO students (name, class, roll_number) VALUES (%s, %s, %s)", (name, class_name, roll_number))
    conn.commit()
    cursor.close()
    conn.close()

def edit_student(student_id, name, class_name, roll_number):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE students SET name=%s, class=%s, roll_number=%s WHERE student_id=%s",
                   (name, class_name, roll_number, student_id))
    conn.commit()
    cursor.close()
    conn.close()

def delete_student(student_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM students WHERE student_id=%s", (student_id,))
    conn.commit()
    cursor.close()
    conn.close()

def add_subject(subject_name):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO subjects (subject_name) VALUES (%s)", (subject_name,))
    conn.commit()
    cursor.close()
    conn.close()

def delete_subject(subject_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM subjects WHERE subject_id=%s", (subject_id,))
    conn.commit()
    cursor.close()
    conn.close()

def add_marks(student_id, subject_id, marks):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO marks (student_id, subject_id, marks) VALUES (%s, %s, %s)", (student_id, subject_id, marks))
    conn.commit()
    cursor.close()
    conn.close()

def edit_marks(mark_id, marks):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE marks SET marks=%s WHERE mark_id=%s", (marks, mark_id))
    conn.commit()
    cursor.close()
    conn.close()

def delete_marks(mark_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM marks WHERE mark_id=%s", (mark_id,))
    conn.commit()
    cursor.close()
    conn.close()

def get_students():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT student_id, name, class, roll_number FROM students")
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result

def get_subjects():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT subject_id, subject_name FROM subjects")
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result

def get_marks(student_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT marks.mark_id, subjects.subject_name, marks.marks "
        "FROM marks JOIN subjects ON marks.subject_id = subjects.subject_id "
        "WHERE marks.student_id = %s", (student_id,))
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result

def get_all_report_cards():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT students.student_id, students.name, students.class, students.roll_number, 
        subjects.subject_name, marks.marks
        FROM marks
        JOIN students ON marks.student_id = students.student_id
        JOIN subjects ON marks.subject_id = subjects.subject_id
    """)
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result
