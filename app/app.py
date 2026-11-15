
import os
import sys

import psycopg2
from psycopg2 import Error

DB_CONFIG = {
    "host": os.environ.get("DB_HOST", "localhost"),
    "port": os.environ.get("DB_PORT", "5432"),
    "dbname": os.environ.get("DB_NAME", "student_db"),
    "user": os.environ.get("DB_USER", "postgres"),
    "password": os.environ.get("DB_PASSWORD", ""),
}


def get_connection():
    return psycopg2.connect(**DB_CONFIG)


def getAllStudents():
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT student_id, first_name, last_name, email, "
                    "enrollment_date FROM students ORDER BY student_id;"
                )
                rows = cur.fetchall()

        print(f"\n{'ID':<5}{'First':<12}{'Last':<12}{'Email':<28}{'Enrolled'}")
        print("-" * 70)
        for sid, first, last, email, enrolled in rows:
            print(f"{sid:<5}{first:<12}{last:<12}{email:<28}{enrolled}")
        print(f"\n{len(rows)} student(s) found.")
    except Error as e:
        print(f"Database error while reading students: {e}")


def addStudent(first_name, last_name, email, enrollment_date):
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO students (first_name, last_name, email, "
                    "enrollment_date) VALUES (%s, %s, %s, %s) "
                    "RETURNING student_id;",
                    (first_name, last_name, email, enrollment_date),
                )
                new_id = cur.fetchone()[0]
        print(f"Student added with ID {new_id}.")
    except Error as e:
        print(f"Could not add student: {e}")


def updateStudentEmail(student_id, new_email):
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "UPDATE students SET email = %s WHERE student_id = %s;",
                    (new_email, student_id),
                )
                if cur.rowcount == 0:
                    print(f"No student found with ID {student_id}.")
                else:
                    print(f"Email updated for student ID {student_id}.")
    except Error as e:
        print(f"Could not update email: {e}")


def deleteStudent(student_id):
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "DELETE FROM students WHERE student_id = %s;",
                    (student_id,),
                )
                if cur.rowcount == 0:
                    print(f"No student found with ID {student_id}.")
                else:
                    print(f"Student ID {student_id} deleted.")
    except Error as e:
        print(f"Could not delete student: {e}")


def read_id(prompt):
    try:
        return int(input(prompt))
    except ValueError:
        print("Please enter a valid whole number.")
        return None


def main():
    try:
        get_connection().close()
    except Error as e:
        print(f"Cannot connect to the database: {e}")
        sys.exit(1)

    while True:
        print("\n===== Student Database =====")
        print("1. Show all students")
        print("2. Add a student")
        print("3. Update a student's email")
        print("4. Delete a student")
        print("5. Quit")
        choice = input("Choose an option (1-5): ").strip()

        if choice == "1":
            getAllStudents()
        elif choice == "2":
            first = input("First name: ").strip()
            last = input("Last name: ").strip()
            email = input("Email: ").strip()
            date = input("Enrollment date (YYYY-MM-DD): ").strip()
            addStudent(first, last, email, date or None)
        elif choice == "3":
            sid = read_id("Student ID: ")
            if sid is not None:
                updateStudentEmail(sid, input("New email: ").strip())
        elif choice == "4":
            sid = read_id("Student ID: ")
            if sid is not None:
                deleteStudent(sid)
        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Invalid choice, please enter 1-5.")


if __name__ == "__main__":
    main()
