from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)

# MySQL connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="your_password",
    database="hospital"
)

# Home page
@app.route('/')
def index():
    cursor = db.cursor()
    cursor.execute("SELECT * FROM patients")
    data = cursor.fetchall()
    return render_template('index.html', patients=data)

# Add patient
@app.route('/add', methods=['GET', 'POST'])
def add_patient():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        disease = request.form['disease']

        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO patients (name, age, disease) VALUES (%s, %s, %s)",
            (name, age, disease)
        )
        db.commit()

        return redirect('/')

    return render_template('add_patient.html')

# DELETE
@app.route('/delete/<int:id>')
def delete_patient(id):
    cursor = db.cursor()
    cursor.execute("DELETE FROM patients WHERE id=%s", (id,))
    db.commit()
    return redirect('/')


# EDIT PAGE
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_patient(id):
    cursor = db.cursor()

    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        disease = request.form['disease']

        cursor.execute(
            "UPDATE patients SET name=%s, age=%s, disease=%s WHERE id=%s",
            (name, age, disease, id)
        )
        db.commit()
        return redirect('/')

    cursor.execute("SELECT * FROM patients WHERE id=%s", (id,))
    patient = cursor.fetchone()
    return render_template('edit_patient.html', p=patient)


# SEARCH
@app.route('/search')
def search():
    query = request.args.get('q')
    cursor = db.cursor()
    cursor.execute("SELECT * FROM patients WHERE name LIKE %s", ('%' + query + '%',))
    data = cursor.fetchall()
    return render_template('index.html', patients=data)

if __name__ == '__main__':
    app.run(debug=True)