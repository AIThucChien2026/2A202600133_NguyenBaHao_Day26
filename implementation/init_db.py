import sqlite3
import os

DB_PATH = "lab_database.db"

def init_db():
    # Remove existing database if it exists to start fresh
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
        print(f"Removed existing database at {DB_PATH}")

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Create tables
    print("Creating tables...")
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        cohort TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS courses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        credits INTEGER NOT NULL
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS enrollments (
        student_id INTEGER,
        course_id INTEGER,
        grade REAL,
        PRIMARY KEY (student_id, course_id),
        FOREIGN KEY (student_id) REFERENCES students (id),
        FOREIGN KEY (course_id) REFERENCES courses (id)
    )
    ''')

    # Seed data
    print("Seeding data...")
    
    students = [
        ('Alice Johnson', 'A1', 'alice@example.com'),
        ('Bob Smith', 'A1', 'bob@example.com'),
        ('Charlie Brown', 'B2', 'charlie@example.com'),
        ('David Wilson', 'B2', 'david@example.com'),
        ('Eve Davis', 'C3', 'eve@example.com')
    ]
    cursor.executemany('INSERT INTO students (name, cohort, email) VALUES (?, ?, ?)', students)

    courses = [
        ('Introduction to Computer Science', 4),
        ('Data Structures and Algorithms', 4),
        ('Database Systems', 3),
        ('Web Development', 3),
        ('Artificial Intelligence', 4)
    ]
    cursor.executemany('INSERT INTO courses (title, credits) VALUES (?, ?)', courses)

    enrollments = [
        (1, 1, 3.8), (1, 2, 4.0), (1, 3, 3.5),
        (2, 1, 3.2), (2, 2, 3.0),
        (3, 3, 3.9), (3, 4, 3.7),
        (4, 4, 3.5), (4, 5, 3.8),
        (5, 1, 4.0), (5, 5, 3.6)
    ]
    cursor.executemany('INSERT INTO enrollments (student_id, course_id, grade) VALUES (?, ?, ?)', enrollments)

    conn.commit()
    conn.close()
    print(f"Database initialized successfully at {DB_PATH}")

if __name__ == "__main__":
    init_db()
