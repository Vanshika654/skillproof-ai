
import sqlite3

DB_NAME = "skillproof.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


def initialize_database():
    conn = get_connection()
    cursor = conn.cursor()

    # Store student profiles
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS profiles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            college TEXT,
            year TEXT,
            target_role TEXT,
            skills TEXT,
            about TEXT
        )
    """)

    # Store assessment results
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS assessments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_name TEXT,
            score INTEGER,
            total INTEGER,
            percentage REAL
        )
    """)

    # Store projects
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            category TEXT,
            description TEXT,
            technologies TEXT,
            github TEXT,
            demo TEXT
        )
    """)

    conn.commit()
    conn.close()


def save_profile(name, college, year, target_role, skills, about):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO profiles
        (name, college, year, target_role, skills, about)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        name,
        college,
        year,
        target_role,
        ", ".join(skills),
        about
    ))

    conn.commit()
    conn.close()


def load_latest_profile():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT name, college, year, target_role, skills, about
        FROM profiles
        ORDER BY id DESC
        LIMIT 1
    """)

    row = cursor.fetchone()
    conn.close()

    if row:
        return {
            "name": row[0] or "",
            "college": row[1] or "",
            "year": row[2] or "",
            "target_role": row[3] or "",
            "skills": [
                skill.strip()
                for skill in (row[4] or "").split(",")
                if skill.strip()
            ],
            "about": row[5] or ""
        }

    return {}


def save_assessment(score, total, percentage, student_name=""):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO assessments
        (student_name, score, total, percentage)
        VALUES (?, ?, ?, ?)
    """, (student_name, score, total, percentage))

    conn.commit()
    conn.close()


def load_latest_assessment():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT score, total, percentage
        FROM assessments
        ORDER BY id DESC
        LIMIT 1
    """)

    row = cursor.fetchone()
    conn.close()

    if row:
        return {
            "score": row[0],
            "total": row[1],
            "percentage": row[2]
        }

    return {}


def save_project(name, category, description, technologies, github, demo):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO projects
        (name, category, description, technologies, github, demo)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (name, category, description, technologies, github, demo))

    conn.commit()
    conn.close()


def load_projects():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, name, category, description, technologies, github, demo
        FROM projects
        ORDER BY id DESC
    """)

    rows = cursor.fetchall()
    conn.close()

    return [
        {
            "id": row[0],
            "name": row[1] or "",
            "category": row[2] or "",
            "description": row[3] or "",
            "technologies": row[4] or "",
            "github": row[5] or "",
            "demo": row[6] or ""
        }
        for row in rows
    ]
