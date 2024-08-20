from flask import Flask, render_template, request, redirect, url_for
import sqlite3, os
from db_setup import create_db

app = Flask(__name__)

create_db()

def get_db_connection():
    if not os.path.exists('data.db'):
        create_db()
    conn = sqlite3.connect('data.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    users = conn.execute('SELECT * FROM users').fetchall()
    conn.close()
    return render_template('index.html', users=users)

@app.route('/users')
def users():
    conn = get_db_connection()
    users = conn.execute('SELECT * FROM users').fetchall()
    conn.close()
    return render_template('users.html', users=users)

@app.route('/create_user', methods=['GET', 'POST'])
def create_user():
    if request.method == 'POST':
        email = request.form['email']
        username = email.split('@')[0]
        company = request.form['company']
        country = request.form['country']
        postcode = request.form['postcode']
        password = username + postcode
        conn = get_db_connection()
        conn.execute('INSERT INTO users (username, email, company, country, postcode, password) VALUES (?, ?, ?, ?, ?, ?)', (username, email, company, country, postcode, password))
        conn.commit()
        conn.close()
        return redirect(url_for('users'))
    return render_template('create_user.html')

@app.route('/update_user/<int:id>', methods=['GET', 'POST'])
def update_user(id):
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE id = ?', (id,)).fetchone()
    if request.method == 'POST':
        email = request.form['email']
        username = email.split('@')[0]
        company = request.form['company']
        country = request.form['country']
        postcode = request.form['postcode']
        password = username + postcode
        conn.execute('UPDATE users SET username = ?, email = ?, company = ?, country = ?, postcode = ?, password = ? WHERE id = ?', (username, email, company, country, postcode, password, id))
        conn.commit()
        conn.close()
        return redirect(url_for('users'))
    conn.close()
    return render_template('update_user.html', user=user)

@app.route('/delete_user/<int:id>')
def delete_user(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM users WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('users'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)