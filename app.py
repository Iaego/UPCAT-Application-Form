from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

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
    # Return the received data for now so the form connection is visible.
    return jsonify(message='Form received. Not yet saved to a database.',
                   application=application)



if __name__ == '__main__':
    app.run(debug=True)
