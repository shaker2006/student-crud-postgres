Python command line application that connects to a PostgreSQL database and performs CRUD operations on a table of students

Demo video: https://youtu.be/65eIh_e3AYQ


PROJECT FILES

- database/schema.sql : creates the students table and inserts the 3 initial rows
- app/app.py : the Python application
- README.md : this file


REQUIREMENTS

- PostgreSQL
- Python 3
- psycopg2

Install the driver on Ubuntu:

    sudo apt install python3-psycopg2


STEP 1: SET UP THE DATABASE

Create the database:

    sudo -u postgres psql -c "CREATE DATABASE student_db;"

Run the schema script (drops and recreates the students table and inserts the initial data):

    cp database/schema.sql /tmp/schema.sql
    sudo -u postgres psql -d student_db -f /tmp/schema.sql

Set a password for the postgres user:

    sudo -u postgres psql -c "ALTER USER postgres PASSWORD 'password';"


STEP 2: SET THE CONNECTION PASSWORD

The application reads the database password from an environment variable so no password is stored in the code:

    export DB_PASSWORD='password'

STEP 3: RUN THE APPLICATION

From the project folder run:

    python3 app/app.py

A menu appears enter 1 to 5 to choose an option


FUNCTIONS

- getAllStudents() : retrieves and displays all records from the students table
- addStudent(first_name, last_name, email, enrollment_date) : inserts a new student record (date format YYYY-MM-DD)
- updateStudentEmail(student_id, new_email) : updates the email address of the student with the given ID
- deleteStudent(student_id) : deletes the record of the student with the given ID


NOTES

- All SQL queries are parameterized to prevent SQL injection
- Database errors are caught and reported without crashing the program
