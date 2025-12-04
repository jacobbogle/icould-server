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

def get_all_users():
    users = load_users()
    kids = load_kids()
    all_users = dict(users)
    for parent_kids in kids.values():
        all_users.update(parent_kids)
    return all_users

def login():
    error = False
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        all_users = get_all_users()
        if username in all_users and all_users[username] == hash_password(password):
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

KIDS_FILE = os.path.join(os.path.dirname(__file__), 'kids.json')

def load_kids():
    if os.path.exists(KIDS_FILE):
        with open(KIDS_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_kids(kids):
    with open(KIDS_FILE, 'w') as f:
        json.dump(kids, f)

def create_kid(parent_username, kid_username, password):
    kids = load_kids()
    if parent_username not in kids:
        kids[parent_username] = {}
    if kid_username in kids[parent_username]:
        return False
    kids[parent_username][kid_username] = hash_password(password)
    save_kids(kids)
    return True

def delete_kid(parent_username, kid_username):
    kids = load_kids()
    if parent_username in kids and kid_username in kids[parent_username]:
        del kids[parent_username][kid_username]
        save_kids(kids)
        return True
    return False

def get_kids_for_user(username):
    kids = load_kids()
    return list(kids.get(username, {}).keys())