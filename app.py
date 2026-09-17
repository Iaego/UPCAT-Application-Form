import sqlite3
from pathlib import Path
from flask import Flask, jsonify, render_template, request


app = Flask(__name__)
DATABASE = Path(app.instance_path) / "applications.squlite3"

def init_db():
    DATABASE.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(DATABASE)

    try:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS applications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                submitted_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                firstName TEXT NOT NULL,
                lastName TEXT NOT NULL,
                middleName TEXT,
                birthday TEXT NOT NULL,
                mother TEXT NOT NULL,
                address TEXT NOT NULL,
                school TEXT NOT NULL,
                strand TEXT NOT NULL,
                schoolAddress TEXT NOT NULL,
                campus1 TEXT NOT NULL,
                program1_1 TEXT NOT NULL,
                program1_2 TEXT NOT NULL,
                program1_3 TEXT NOT NULL,
                program1_4 TEXT NOT NULL,
                campus2 TEXT NOT NULL,
                program2_1 TEXT NOT NULL,
                program2_2 TEXT NOT NULL,
                program2_3 TEXT NOT NULL,
                program2_4 TEXT NOT NULL
            )
        """)
        connection.commit()
    finally:
        connection.close()

init_db()

@app.route('/')
def home():
    return render_template('design.html')

@app.post('/applications')
def submit_application():
    # These keys match the name attributes of the HTML inputs.
    field_names = (
        'firstName', 'lastName', 'middleName', 'birthday', 'mother',
        'address', 'school', 'strand', 'schoolAddress',
        'campus1', 'program1_1', 'program1_2', 'program1_3', 'program1_4',
        'campus2', 'program2_1', 'program2_2', 'program2_3', 'program2_4',
    )
    application = {
        name: request.form.get(name, '').strip()
        for name in field_names
    }

    missing_fields = [
        name for name in field_names
        if name != 'middleName' and not application[name]
    ]
    if missing_fields:
        return jsonify(error='Please complete all required fields.',
                       missing_fields=missing_fields), 400

    # Add database saving here; application contains the submitted values.
    connection = sqlite3.connect(DATABASE)

    try:
        cursor = connection.execute("""
            INSERT INTO applications (
                firstName, lastName, middleName, birthday, mother,
                address, school, strand, schoolAddress,
                campus1, program1_1, program1_2, program1_3, program1_4,
                campus2, program2_1, program2_2, program2_3, program2_4
            )
            VALUES (
                ?, ?, ?, ?, ?,
                ?, ?, ?, ?,
                ?, ?, ?, ?, ?,
                ?, ?, ?, ?, ?
            )
        """, tuple(application[name] for name in field_names))

        connection.commit()
        application_id = cursor.lastrowid

    except sqlite3.Error:
        connection.rollback()
        app.logger.exception("Could not save application")
        return jsonify(error="Could not save your application."), 500

    finally:
        connection.close()

    return jsonify(
        message="Application saved successfully.",
        application_id=application_id
    ), 201



if __name__ == '__main__':
    app.run(debug=True)
