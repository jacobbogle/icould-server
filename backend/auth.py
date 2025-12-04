from flask import session, redirect, url_for, request, render_template
import os
import json
import hashlib

USERS_FILE = os.path.join(os.path.dirname(__file__), 'users.json')

def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'r') as f:
            users = json.load(f)
            if not users:
                users = {'admin': hash_password('password')}
                save_users(users)
            return users
    users = {'admin': hash_password('password')}
    save_users(users)
    return users

def save_users(users):
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def get_admin_password():
    users = load_users()
    return users.get('admin', 'password')

def set_admin_password(new_password):
    users = load_users()
    users['admin'] = hash_password(new_password)
    save_users(users)

def login_required(f):
    def wrapper(*args, **kwargs):
        if not session.get('username'):
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    wrapper.__name__ = f.__name__
    return wrapper

def login():
    error = False
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = load_users()
        if username in users and users[username] == hash_password(password):
            session['username'] = username
            return redirect(url_for('index'))
        else:
            error = True
    return render_template('login.html', error=error)

def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

def change_password():
    username = session.get('username')
    if not username:
        return redirect(url_for('login'))
    if request.method == 'POST':
        current = request.form['current_password']
        new = request.form['new_password']
        confirm = request.form['confirm_password']
        users = load_users()
        if users.get(username) == hash_password(current) and new == confirm:
            users[username] = hash_password(new)
            save_users(users)
            return redirect(url_for('index'))
        else:
            error = "Invalid current password or passwords do not match."
            return render_template('change_password.html', error=error)
    return render_template('change_password.html')

def create_user(username, password):
    users = load_users()
    if username in users:
        return False
    users[username] = hash_password(password)
    save_users(users)
    return True

def delete_user(username):
    users = load_users()
    if username in users and username != 'admin':
        del users[username]
        save_users(users)
        return True
    return False

def get_users():
    return list(load_users().keys())