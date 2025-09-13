from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Create database and table if not exists
conn = sqlite3.connect('users.db', check_same_thread=False)
conn.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    email TEXT,
    password TEXT
)
''')
conn.commit()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/save', methods=['POST'])
def save_user():
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']

    conn.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)", (name, email, password))
    conn.commit()
    return redirect(url_for('list_users'))

@app.route('/users')
def list_users():
    cursor = conn.execute("SELECT * FROM users")
    users = cursor.fetchall()
    return render_template('users.html', users=users)

@app.route('/delete/<int:user_id>')
def delete_user(user_id):
    conn.execute("DELETE FROM users WHERE id=?", (user_id,))
    conn.commit()
    return redirect(url_for('list_users'))

if __name__ == '__main__':
    app.run(debug=True)
