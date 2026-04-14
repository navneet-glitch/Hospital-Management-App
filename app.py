from flask import Flask, render_template, request, redirect, session
import mysql.connector

app = Flask(__name__)
app.secret_key = "secret123"

# MySQL connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Navya@MYSQL2026",   # apna password daalna
    database="hospital"
)

# ===========================
# LOGIN REQUIRED DECORATOR
# ===========================
def login_required(func):
    def wrapper(*args, **kwargs):
        if 'user' not in session:
            return redirect('/login')
        return func(*args, **kwargs)
    wrapper.__name__ = func.__name__
    return wrapper


# ===========================
# HOME PAGE
# ===========================
@app.route('/')
@login_required
def index():
    cursor = db.cursor()
    cursor.execute("SELECT * FROM patients")
    data = cursor.fetchall()
    return render_template('index.html', patients=data)


# ===========================
# SIGNUP
# ===========================
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']
        email = request.form['email']
        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO users (email, name, password) VALUES (%s, %s, %s)",
            (email, name, password)
        )
        db.commit()

        return redirect('/login')

    return render_template('signup.html')


# ===========================
# LOGIN
# ===========================
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        password = request.form['password']
        email = request.form['email']
        cursor = db.cursor()
        cursor.execute(
            "SELECT * FROM users WHERE email=%s AND password=%s",
            (email, password)
        )
        user = cursor.fetchone()

        if user:
            session['user'] = email
            return redirect('/')
        else:
            return "Invalid email or password ❌"

    return render_template('signin.html')


# ===========================
# LOGOUT
# ===========================
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/login')


# ===========================
# ADD PATIENT
# ===========================
@app.route('/add', methods=['GET', 'POST'])
@login_required
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


# ===========================
# DELETE
# ===========================
@app.route('/delete/<int:id>')
@login_required
def delete_patient(id):
    cursor = db.cursor()
    cursor.execute("DELETE FROM patients WHERE id=%s", (id,))
    db.commit()
    return redirect('/')


# ===========================
# EDIT
# ===========================
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
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


# ===========================
# SEARCH
# ===========================
@app.route('/search')
@login_required
def search():
    query = request.args.get('q')
    cursor = db.cursor()
    cursor.execute(
        "SELECT * FROM patients WHERE name LIKE %s",
        ('%' + query + '%',)
    )
    data = cursor.fetchall()
    return render_template('index.html', patients=data)

@app.route('/doctors')
@login_required
def doctors():
    cursor = db.cursor()
    cursor.execute("SELECT * FROM doctors")
    data = cursor.fetchall()
    return render_template('doctors.html', doctors=data)


# ===========================
# RUN APP
# ===========================
if __name__ == '__main__':
    app.run(debug=True)