from flask import Flask, render_template_string, request, redirect, url_for
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
    # Example usage of get_db_connection
    conn = get_db_connection()
    users = conn.execute('SELECT * FROM users').fetchall()
    conn.close()
    return str(users)

@app.route('/users')
def users():
    conn = get_db_connection()
    users = conn.execute('SELECT * FROM users').fetchall()
    conn.close()
    html = '''
    <h1>Users</h1>
    <table border="1">
        <tr>
            <th>Username</th>
            <th>Email</th>
            <th>company</th>
            <th>country</th>
            <th>postcode</th>
            <th>password</th>
            <th>Actions</th>
        </tr>
    '''
# - username
# - email
# - company
# - country
# - postcode
# - password
    for user in users:
        html += f'''
        <tr>
            <td>{user["username"]}</td>
            <td>{user["email"]}</td>
            <td>{user["company"]}</td>
            <td>{user["country"]}</td>
            <td>{user["postcode"]}</td>
            <td>{user["password"]}</td>
            <td>
                <a href="/update_user/{user["id"]}">Update</a>
                <a href="/delete_user/{user["id"]}">Delete</a>
            </td>
        </tr>
        '''
    html += '''
    </table>
    <br>
    <a href="/create_user">Create New User</a>
    '''
    return render_template_string(html)

@app.route('/create_user', methods=['GET', 'POST'])
def create_user():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        conn = get_db_connection()
        conn.execute('INSERT INTO users (username, email) VALUES (?, ?)', (username, email))
        conn.commit()
        conn.close()
        return redirect(url_for('users'))
    return render_template_string('''
    <h1>Create User</h1>
    <form method="post">
        Username: <input type="text" name="username"><br>
        Email: <input type="text" name="email"><br>
        <input type="submit" value="Create">
    </form>
    <a href="/users">Back to Users</a>
    ''')

@app.route('/update_user/<int:id>', methods=['GET', 'POST'])
def update_user(id):
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE id = ?', (id,)).fetchone()
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        conn.execute('UPDATE users SET username = ?, email = ? WHERE id = ?', (username, email, id))
        conn.commit()
        conn.close()
        return redirect(url_for('users'))
    conn.close()
    return render_template_string('''
    <h1>Update User</h1>
    <form method="post">
        Username: <input type="text" name="username" value="{{ user['username'] }}"><br>
        Email: <input type="text" name="email" value="{{ user['email'] }}"><br>
        <input type="submit" value="Update">
    </form>
    <a href="/users">Back to Users</a>
    ''', user=user)

@app.route('/delete_user/<int:id>')
def delete_user(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM users WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('users'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)