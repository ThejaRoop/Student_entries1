from flask import Flask, render_template, request, redirect, url_for, flash, g
import sqlite3

app = Flask(__name__)
app.secret_key = 'secret_key'

# Function to get the database connection
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect('example.db')
    return db

# Create the database tables if they don't exist
def create_tables():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            age INTEGER
        )
    ''')
    conn.commit()

# Route for home page
@app.route('/')
def home():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()
    return render_template('index.html', students=students)

# Route for creating a student
@app.route('/create', methods=['POST'])
def create():
    name = request.form['name']
    age = request.form['age']
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO students (name, age) VALUES (?, ?)", (name, age))
    conn.commit()
    flash('Student created successfully.', 'success')
    return redirect(url_for('home'))

if __name__ == '__main__':
    with app.app_context():
        create_tables()
    app.run(debug=True)
